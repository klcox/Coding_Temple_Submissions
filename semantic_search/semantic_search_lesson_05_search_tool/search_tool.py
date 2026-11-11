import streamlit as st
import chromadb
import os


# ===========
# PAGE CONFIG
# ===========


st.set_page_config(
    page_title="Semantic Search", 
    page_icon="🔍", 
    layout="wide"
)


# ==============
# CHROMADB SETUP
# ==============


@st.cache_resource
def get_collection():
    """Set up a persistent ChromaDB client and retrive or create the collection."""

    client = chromadb.PersistentClient(path="./search_db")

    return client.get_or_create_collection(
        name="course_docs", 
        configuration={"hnsw": {"space": "cosine"}}
    )

collection = get_collection()


if "sources" not in st.session_state:  # Store sources in state if they have not been initialized

    metadata_response = collection.get(
        include=["metadatas"]
    )    

    sources_set = set(metadata["source"] for metadata in metadata_response["metadatas"])

    st.session_state["sources"] = sources_set


# ==================
# LOADING & CHUNKING
# ==================


def load_and_chunk(directory):
    """Load text files and split them into chunks."""

    chunks = []

    for filename in sorted(os.listdir(directory)):

        if not filename.endswith((".txt", ".md")):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()

        # Split by paragraphs (double newline)
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        for i, para in enumerate(paragraphs):
            chunks.append({
                "text": para,
                "source": filename,
                "chunk_id": f"{filename}_{i}",
                "chunk_index": i,
            })

    return chunks


# =======
# SIDEBAR
# =======


with st.sidebar:

    st.title("📁 Document Manager")

    if st.button("🔄 Re-index Documents"):

        with st.spinner(
            "Loading documents",
            show_time=False,
        ):
            chunks = load_and_chunk("docs")

        if chunks:  # If there are chunks available, add them to the collection

            collection.upsert(
                documents=[chunk["text"] for chunk in chunks],
                metadatas=[{"source": chunk["source"], "chunk_index": str(chunk["chunk_index"])} for chunk in chunks],
                ids=[chunk["chunk_id"] for chunk in chunks],
            )            
            st.session_state["sources"] = set(chunk["source"] for chunk in chunks)

            st.success(f"Indexed {len(chunks)} chunks from {len(st.session_state['sources'])} files")
        
        else:
            st.warning("No .txt or .md files found in docs/ folder")


    st.metric(
        "Documents in Database", 
        collection.count()
    )

    st.metric(
        "Files in Database",
        len(st.session_state["sources"])
    )

    st.divider()


    n_results_setting = st.slider("Number of Results to Display", 1, 10, 5)

    source_select = st.multiselect(
        "Search only these sources",
        sorted(st.session_state["sources"])  # Converts set into a sorted list
    )


# ==============
# MAIN INTERFACE
# ==============


st.title("🔍 Semantic Search")

st.write("Search course documents by meaning rather than keywords.")

st.space("small")


query = st.text_input("Enter your search query", placeholder="What is an HTML tag?")

if query and collection.count() > 0:  # If the user has entered a query and there are docs in the collection

    if len(source_select) >= 2:    
        source_select_dicts = [{"source": selection} for selection in source_select]
        source_select_filter = {"$or": source_select_dicts}

    elif len(source_select) == 1:
        source_select_filter = {"source": source_select[0]}

    else:
        source_select_filter = None
    
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results_setting, collection.count()),
        where=source_select_filter
    )


    st.space("small")

    
    if not results["documents"][0]:
        st.info("No results found in the selected sources. Try adjusting your query or the selected sources.")
    
    else:  
        st.subheader(f"Top {len(results['documents'][0])} Results")   
        st.caption(f"*Out of {collection.count()} total database documents*") 

        st.write("Result Relevance: 🟢 High  🟡 Medium  🔴 Low")

        st.space("small")
        
        
        for i in range(len(results['documents'][0])):

            doc = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]

            # Color-code by relevance
            if distance < 0.5:
                relevance = "🟢"
            elif distance < 1.0:
                relevance = "🟡"
            else:
                relevance = "🔴"

            with st.container():

                col_meta, col_score = st.columns([3, 1])

                with col_meta:
                    st.write(f"From: **{metadata['source']}** — Chunk {metadata['chunk_index']}")

                with col_score:
                    st.write(f"{relevance} (dist: {distance:.3f})")


                if len(doc) > 150:

                    st.write(f"{doc[:150] + ' ...'}")

                    with st.expander(
                        "See full text"
                    ):               
                        st.write(doc)
                
                else:
                    st.write(doc)
                            
                st.divider()

elif collection.count() == 0:  # If there are no docs in the collection
    st.info("👈 Click 'Re-index Documents' in the sidebar to load your documents first.")