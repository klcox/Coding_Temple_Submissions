from ingest import get_collection, load_and_chunk, get_embedding_model, embed_chunks


eval_set = [
    {
        "query": "What is needed for an API request?",
        "relevant": ["fastapi.txt", "rest-apis.txt"]
    },
    {
        "query": "How does Streamlit remember data between interactions?",
        "relevant": ["streamlit.txt"]
    },
    {
        "query": "What is cosine similarity?",
        "relevant": ["embeddings-and-vectors.txt"]
    },
    {
        "query": "How are Python and SQL related?",
        "relevant": ["sql-databases.txt"]
    },
    {
        "query": "What is a virtual environment?",
        "relevant": ["python-fundamentals.txt"]
    }
]


def prepare_collection_for_eval(chunk_size):
    """Get/create the collection; load/chunk documents according to the designated chunk size; and store in ChromaDB database."""

    collection = get_collection()

    chunks = load_and_chunk("docs", chunk_size, overlap=50)

    if chunks:  # If there are chunks available, embed them and add them to the collection

        chunks_with_embeddings = embed_chunks(chunks)


        existing_ids = collection.get()["ids"]

        if existing_ids:
            collection.delete(ids=existing_ids)  # If applicable, delete old collection so as to cleanly reflect new chunk size


        collection.upsert(
            documents=[chunk["text"] for chunk in chunks_with_embeddings],
            embeddings=[chunk["embedded_chunk"] for chunk in chunks_with_embeddings],
            metadatas=[{"source": chunk["source"], "chunk_index": str(chunk["chunk_index"]), "chunk_size": chunk["chunk_size"]} for chunk in chunks_with_embeddings],
            ids=[chunk["chunk_id"] for chunk in chunks_with_embeddings],
        )
        
        return collection
    
    else:
        return None


def evaluate(collection, eval_set):
    """Run evaluation and compute precision/recall."""
    
    model = get_embedding_model()

  
    for i, item in enumerate(eval_set):

        query = item["query"]
        print(f"\nQuery {i + 1}: {query}")
        
        query_embedding = model.encode(query)
        
        relevant = set(item["relevant"])

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        returned = {
            metadata["source"]
            for metadata in results["metadatas"][0]
        }
       
        # Precision: of the documents returned, how many are relevant?
        correct_results = returned & relevant  # & checks for shared values in both variables
        precision = len(correct_results) / len(returned) if returned else 0  # If the number of shared values is less than the number of results returned = low precision

        # Recall: of the relevant documents, how many were returned?
        recall = len(correct_results) / len(relevant) if relevant else 0  # If the number of shared values is less than the number of results declared relevant = low recall 

        print(f"  P={precision:.1%}  R={recall:.1%}")

        print("\n  Top 3 Results:")
        for i, result in enumerate(results["documents"][0]):
            print(f"    {results['distances'][0][i]:.3f}, {result.replace('\n\n', '//')[:100] + '...'}")           


# Run evaluation

for chunk_size in [150, 300]:

    collection = prepare_collection_for_eval(chunk_size)

    if collection:
        print(f"\n=== Evaluation at Chunk Size: {chunk_size} ===")

        evaluate(collection, eval_set)

    else:
        print("Could not obtain collection.")