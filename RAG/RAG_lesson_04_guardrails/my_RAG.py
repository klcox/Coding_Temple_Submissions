import chromadb
import requests
from requests import HTTPError
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


def retrieve(collection, query, n_results=3, threshold=1.0):
    """Search ChromaDB and retrieve relevant document chunks."""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    chunks = []

    for i in range(len(results["documents"][0])):

        if results["distances"][0][i] <= threshold:

            chunks.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

    return chunks


# ====================
# CONFIDENCE INDICATOR
# ====================


def get_confidence(chunks):
    """Return a confidence indicator and icon."""    
    
    if not chunks:
        return "None", "🔴"
    
    best = chunks[0]["distance"]

    if best < 0.5:
        return "High", "🟢"
    
    elif best < 1.0:
        return "Medium", "🟡"
    
    else:
        return "Low", "🔴"


# ============
# BUILD PROMPT
# ============


SYSTEM_PROMPT = """You are a helpful AI assistant for students learning AI engineering.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section for your response.
- NEVER make up information not present in the context.
- If context is None, your answer should be the following: 'Sorry, I don't have relevant information to answer that.'
- If context is provided but does not contain the answer or if you are not sure, do NOT guess. Instead say: 'I don't have enough information to answer that based on the available documents.'
- Otherwise, if you are able to answer from the context alone, always cite your source(s) by mentioning the document name(s) in parentheses, and keep your response under 200 words.
"""

def build_messages(question, retrieved_chunks):
    """Build the RAG prompt with retrieved context."""

    context_parts = []

    if retrieved_chunks:
        for chunk in retrieved_chunks:        
            source = chunk["metadata"]["source"]
            context_parts.append(f"[Source: {source}]\n{chunk['text']}")

        context = "\n\n---\n\n".join(context_parts)

    else:
        context = None

    system_with_context = f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"

    return [
        {"role": "system", "content": system_with_context},
        {"role": "user", "content": question}
    ]


# =================
# GENERATE RESPONSE
# =================


def generate(messages, stream=False):
    """Call Ollama to generate a response."""
    
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL,
            "messages": messages,
            "stream": stream
        }, stream=stream)  # Both Ollama and requests need stream=True 

        response.raise_for_status()       

    except requests.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running?"

    except HTTPError as err_msg:
        return f"ERROR: {err_msg}"

    return response


# ================
# DISPLAY RESPONSE
# ================


def display_response(response_info):
    """Display the number of chunks retrieved, sources, confidence indicators, and the response."""
    
    print(f"\nRetrieved {response_info['chunks_retrieved']} chunks below the threshold.")
    print(f"\nSources: {response_info['sources'] if response_info['sources'] else 'N/A'}")
    print(f"\nRetrieval Confidence: {response_info['icon']} {response_info['confidence']}")
    
    
    print(f"\nAnswer (streaming):\n")


    # -------------------
    # NO CHUNKS RETRIEVED
    # -------------------

    if response_info["chunks_retrieved"] == 0:
        answer = response_info["answer"]

        if response_info["stream"]:  # If stream = True
            for char in answer:

                print(char, end="", flush=True)
                time.sleep(0.02)  # Simulate streaming

            print()

        else:  # If stream = False
            print(answer)

        return answer


    # -------------
    # ERROR MESSAGE
    # -------------

    if isinstance(response_info["answer"], str):
        print(response_info["answer"])
        return response_info["answer"]


    # ----------------
    # CHUNKS RETRIEVED
    # ----------------

    if response_info['stream']:  # If stream = True
        full_response = ""

        for line in response_info['answer'].iter_lines():  # Read each line of the response one at a time

            if line:
                data = json.loads(line)  # Converts JSON to a Python dictionary
                token = data.get("message", {}).get("content", "")

                if token:
                    print(token, end="", flush=True)  # end="" prevents each token from printing on a new line; flush=True displays the text immediately
                    full_response += token
        
        print()  # New line after streaming

        return full_response
    
    else:  # If stream = False
        return response_info['answer'].json()["message"]["content"]


# ============
# RAG PIPELINE
# ============


def rag_query(collection, question, n_results=3, stream=True, threshold=1.0):
    """Complete RAG pipeline: retrieve + build prompt + generate."""

    print(f"\n{'=' * 60} Question: {question} {'=' * 60}")
   

    # ---------------
    # RETRIEVE CHUNKS
    # ---------------

    chunks = retrieve(collection, question, n_results, threshold)


    # ------------------------
    # GET CONFIDENCE INDICATOR
    # ------------------------

    confidence, icon = get_confidence(chunks)    


    if not chunks:
        return {
            "answer": "I don't have relevant information to answer that.",
            "sources": [],
            "confidence": confidence,
            "icon": icon,
            "chunks_retrieved": len(chunks),
            "stream": stream
        }            
       

    # ------
    # PROMPT
    # ------

    messages = build_messages(question, chunks)


    # -----------------
    # GENERATE RESPONSE
    # -----------------
   

    start = time.time()

    response = generate(messages, stream=stream)

    elapsed = time.time() - start

    print(f"\n[Generated response in {elapsed:.1f}s]")

    sources = {chunk["metadata"]["source"] for chunk in chunks}

    return {
        "answer": response,
        "sources": sources,
        "confidence": confidence,
        "icon": icon,
        "chunks_retrieved": len(chunks),
        "stream": stream
    }


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
            response_info = rag_query(collection, question)
            display_response(response_info)