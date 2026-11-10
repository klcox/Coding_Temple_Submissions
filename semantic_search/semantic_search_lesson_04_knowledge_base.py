import chromadb


client = chromadb.PersistentClient(path="./chroma_demo")  # Establish persistent client

collection = client.get_or_create_collection(  # If collection exists, get it; otherwise, create it
    name="my_knowledge",
    metadata={"description": "AI Software Engineering course content"},
    configuration={"hnsw": {"space": "cosine"}}
)


# ====
# DATA
# ====


documents = [
    # Module 1 — AI Fundamentals
    "Large language models are pre-trained on internet text and fine-tuned to follow instructions.",
    "Tokens are the units an LLM processes; a token is roughly 4 characters or ¾ of a word.",
    "Temperature controls randomness in model outputs: 0 is deterministic, 1 is creative.",

    # Module 3 — Databases
    "SQL SELECT with JOIN retrieves related rows from multiple tables based on matching keys.",
    "An index on a frequently queried column dramatically speeds up SELECT statements.",
    "Transactions use COMMIT and ROLLBACK to ensure groups of operations are atomic.",

    # Module 4 — REST APIs
    "REST uses HTTP verbs: GET to read, POST to create, PUT to update, DELETE to remove.",
    "Status codes communicate outcomes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found.",
    "Authentication tokens like JWTs are passed in the Authorization header of HTTP requests.",

    # Module 5 — FastAPI
    "FastAPI generates interactive OpenAPI documentation automatically from route definitions.",
    "Pydantic BaseModel validates incoming JSON bodies and returns clear error messages on failure.",
    "Background tasks in FastAPI run after a response is returned, keeping endpoints fast.",

    # Module 6 — Streamlit
    "Streamlit re-runs the entire script from top to bottom on every widget interaction.",
    "st.session_state stores values that persist across script re-runs within a user session.",
    "st.cache_resource caches objects like ML models so they are only loaded once.",
]

metadatas = [
    {"module": "1", "topic": "ai"},
    {"module": "1", "topic": "ai"},
    {"module": "1", "topic": "ai"},
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "database"},
    {"module": "4", "topic": "api"},
    {"module": "4", "topic": "api"},
    {"module": "4", "topic": "api"},
    {"module": "5", "topic": "api"},
    {"module": "5", "topic": "api"},
    {"module": "5", "topic": "api"},
    {"module": "6", "topic": "frontend"},
    {"module": "6", "topic": "frontend"},
    {"module": "6", "topic": "frontend"},
]

ids = [f"doc_{i}" for i in range(len(documents))]

collection.upsert(  # .upsert instead of .add allows updating existing documents in the collection
    documents=documents,
    metadatas=metadatas,
    ids=ids
)


# ======
# SEARCH
# ======


def search(query: str, n_results: int = 5, module_filter: str = None):
    """Return the top n_results for the query, optionally filtered to a specific module."""

    where_filter = {"module": module_filter} if module_filter else None

    results = collection.query(
        query_texts = [query],
        n_results = n_results,
        where=where_filter
    )

    print(f"  {'Rank':<4} | {'Distance':<8} | {'Metadata':<26} | {'Doc Text':<53}")
    print(f"  {'-' * 100}")
    for i in range(len(results["documents"][0])):        
        distance = results['distances'][0][i]  # Lower distance = greater similarity
        metadata = results['metadatas'][0][i]
        metadata_text = f"Module: {metadata['module']}, Topic: {metadata['topic']}"
        doc_text = results['documents'][0][i]

        print(f"  {i+1:<4} | {distance:<8.3f} | {metadata_text:<26} | {doc_text[:50] + "..."}")


# =======
# QUERIES
# =======

   
print("=== Broad Query (no filter) ===")
query = "How do applications use databases and APIs to process and manage information?"
print(f"Query: {query}\n")
search(query)

print("\n=== Query Filtered to a Specific Module ===")
query = "What kind of error messages or responses can an API return?"
print(f"Query: {query} (Filtered to Module 4)\n")
search(query, module_filter="4")

print("\n=== Query Using Different Words Than the Stored Documents ===")
query = "What happens when a user performs an action on a Streamlit application?"
print(f"Query: {query}\n")
search(query)