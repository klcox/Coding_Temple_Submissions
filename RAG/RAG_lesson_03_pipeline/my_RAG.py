import chromadb
import requests
import json
import os
import time


OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"  


# =========
# INGESTION
# =========


def load_documents(directory):
    """Load all .txt and .md files from a directory."""

    docs = []

    for filename in sorted(os.listdir(directory)):

        if filename.endswith((".txt", ".md")):

            with open(os.path.join(directory, filename), "r") as f:
                content = f.read()

            # Split by paragraphs for chunking
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

            for i, para in enumerate(paragraphs):
                docs.append({
                    "text": para,
                    "id": f"{filename}_{i}",
                    "metadata": {"source": filename, "chunk_index": str(i)}
                })

    return docs


def ingest(collection, docs_directory):
    """Load, chunk, and store documents in ChromaDB."""
    
    chunks = load_documents(docs_directory)

    if not chunks:
        print("No documents found!")
        return 0

    collection.upsert(
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        ids=[chunk["id"] for chunk in chunks]
    )
    return len(chunks)


# =========
# RETRIEVAL
# =========


def retrieve(collection, query, n_results=3):
    """Search ChromaDB for relevant document chunks."""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    chunks = []

    for i in range(len(results["documents"][0])):

        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return chunks


# ============
# BUILD PROMPT
# ============


SYSTEM_PROMPT = """You are a helpful AI assistant for students learning AI engineering.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section.
- If the context doesn't contain the answer, say "I don't have enough information
  to answer that based on the available documents."
- Cite your sources by mentioning the document name in parentheses.
- Keep your response under 200 words.
"""

def build_messages(question, retrieved_chunks):
    """Build the RAG prompt with retrieved context."""

    context_parts = []

    for chunk in retrieved_chunks:        
        source = chunk["metadata"]["source"]
        context_parts.append(f"[Source: {source}]\n{chunk['text']}")

    context = "\n\n---\n\n".join(context_parts)
    system_with_context = f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"

    return [
        {"role": "system", "content": system_with_context},
        {"role": "user", "content": question}
    ]


# ===================
# RESPONSE GENERATION
# ===================


def generate(messages, stream=False):
    """Call Ollama to generate a response."""
    
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL,
            "messages": messages,
            "stream": stream
        }, stream=stream)  # Both Ollama and requests need stream=True

        if stream:
            full_response = ""

            for line in response.iter_lines():  # Read each line of the response one at a time

                if line:
                    data = json.loads(line)  # Converts JSON to a Python dictionary
                    token = data.get("message", {}).get("content", "")

                    if token:
                        print(token, end="", flush=True)  # end="" prevents each token from printing on a new line; flush=True displays the text immediately
                        full_response += token
            
            print()  # New line after streaming

            return full_response
        
        else:
            return response.json()["message"]["content"]

    except requests.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running?"
    

# ============
# RAG PIPELINE
# ============


def rag_query(collection, question, n_results=3, stream=True):
    """Complete RAG pipeline: retrieve + build prompt + generate."""

    print(f"\n{'=' * 60} Question: {question} {'=' * 60}")
   

    # --------
    # RETRIEVE
    # --------

    chunks = retrieve(collection, question, n_results)

    print(f"\nRetrieved {len(chunks)} chunks:")

    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}] (dist: {chunk['distance']:.3f}) {chunk['metadata']['source']}")


    # ------
    # PROMPT
    # ------

    messages = build_messages(question, chunks)


    # -----------------
    # GENERATE RESPONSE
    # -----------------

    print(f"\nAnswer (streaming):\n")

    start = time.time()

    answer = generate(messages, stream=stream)

    elapsed = time.time() - start

    print(f"\n[Generated in {elapsed:.1f}s]")

    return answer


# ====
# MAIN
# ====


if __name__ == "__main__":

    # -------------
    # CHROMA CLIENT
    # -------------

    client = chromadb.PersistentClient(path="./my_RAG_db")

    collection = client.get_or_create_collection(
        name="course_docs", 
        configuration={"hnsw": {"space": "cosine"}}
    )    


    # ------
    # INGEST
    # ------

    if collection.count() == 0:  # Ingest only if a collection does not already exist
        count = ingest(collection, "RAG_lesson_03_pipeline/docs")

        print(f"Ingested {count} document chunks.")

    else:
        print(f"Using existing collection: {collection.count()} chunks")


    # ---------
    # INTERFACE
    # ---------

    print("\nRAG Pipeline Ready! Ask questions about your documents.")    
    print("Type 'quit' to exit.\n")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ('quit', 'exit', 'q'):
            break

        if question:
            rag_query(collection, question)