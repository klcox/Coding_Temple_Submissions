import chromadb


# =============
# DOCUMENT INFO
# =============


documents = {
    "doc_jwt": "JWT tokens provide stateless authentication for REST APIs. The server creates a signed token containing user info.",
    "doc_pydantic": "Pydantic models define data schemas for FastAPI. They automatically validate incoming request data.",
    "doc_session": "Streamlit session state persists data across re-runs. Initialize with: if key not in st.session_state.",
    "doc_cors": "CORS middleware in FastAPI allows cross-origin requests from frontend applications running on different ports.",
    "doc_embed": "Embeddings convert text into numerical vectors capturing semantic meaning. Similar texts get similar vectors.",
    "doc_cosine": "Cosine similarity measures the angle between two vectors. A score of 1.0 means identical direction.",
    "doc_chunk": "Chunking splits documents into smaller pieces for embedding. Chunk size affects search precision and recall.",
    "doc_chroma": "ChromaDB is a vector database for storing and querying embeddings. It supports metadata filtering.",
    "doc_flex": "CSS Flexbox arranges elements in rows or columns. Use display:flex on the container.",
    "doc_dom": "The DOM is the browser's tree representation of HTML. JavaScript uses it to modify page content.",
    "doc_html": "HTML uses tags to mark up content. A tag is a keyword wrapped in angle brackets: <p>This is a paragraph.</p>",
    "doc_css": "CSS stands for Cascading Style Sheets. It's the language that controls how HTML elements look - colors, fonts, spacing, sizes, and layout."
}

doc_ids = list(documents.keys())
doc_texts = list(documents.values())


# =============
# CHROMA CLIENT
# =============


client = chromadb.PersistentClient(path="./eval_demo")

collection = client.get_or_create_collection(
    name="course_docs",
    configuration={"hnsw": {"space": "cosine"}}
)

collection.upsert(
    documents=doc_texts,
    ids=doc_ids
)


# ==========
# EVALUATION
# ==========


eval_set = [
    {
        "query": "How do I authenticate API requests?",
        "relevant": ["doc_jwt", "doc_cors"]
    },
    {
        "query": "How does Streamlit remember data between interactions?",
        "relevant": ["doc_session"]
    },
    {
        "query": "What is semantic similarity and how is it measured?",
        "relevant": ["doc_embed", "doc_cosine"]
    },
    {
        "query": "How should I prepare documents for a search system?",
        "relevant": ["doc_chunk", "doc_chroma"]
    },
    {
        "query": "How do I make a webpage interactive?",
        "relevant": ["doc_dom", "doc_flex", "doc_css", "doc_html"]
    },
    {
        "query": "How do I style a webpage?",
        "relevant": ["doc_css", "doc_flex"]
    },
]


def evaluate(eval_set, threshold, n_results=5):
    """Run evaluation and compute precision/recall for both individual queries and the overall average."""

    total_precision = 0
    total_recall = 0

    print(f"\n=== Evaluation at threshold={threshold}, n_results={n_results} ===")  

    for i, item in enumerate(eval_set):
        query = item["query"]
        relevant = set(item["relevant"])

        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        returned = {
            results["ids"][0][j]
            for j, dist in enumerate(results["distances"][0])
            if dist <= threshold  # ChromaDB: lower distance = greater similarity
        }
       
        # Precision: of the documents returned, how many are relevant?
        true_positives = returned & relevant  # & checks for shared values in both variables
        precision = len(true_positives) / len(returned) if returned else 0  # If the number of shared values is less than the number of results returned = low precision

        # Recall: of the relevant documents, how many were returned?
        recall = len(true_positives) / len(relevant) if relevant else 0  # If the number of shared values is less than the number of results declared relevant = low recall 

        # Tabulation for average calculation
        total_precision += precision
        total_recall += recall

        print(f"Query {i + 1}: P={precision:.1%}  R={recall:.1%}")     

    avg_precision = total_precision / len(eval_set)
    avg_recall = total_recall / len(eval_set)

    print(f"\nAVERAGE P={avg_precision:.1%}  R={avg_recall:.1%}")


for threshold in [0.55, 0.7, 0.9]:
    evaluate(eval_set, threshold=threshold)


# ========
# ANALYSIS
# ========


print("""\nANALYSIS:
 - The first 3 queries (pertaining to API authentication, Streamlit, and semantic similarity) worked well, especially at lower thresholds.
 - The last 3 queries (pertaining to document preparation and webpages) performed much less consistently, even returning 0% precision and recall scores at the lowest threshold.
 - Overall, we can see that stricter thresholds result in greater precision (lower recall) and vice versa - looser thresholds result in lower precision (greater recall).
 - To improve scores, I would refine document descriptions (possibly adding more context), improve query wording, review relevance labels, and experiment with distance thresholds to find the best fit for the collection.
""")