import os
from sentence_transformers import SentenceTransformer
import chromadb
import streamlit as st


# =============================
# FUNCTIONS: LOAD, CHUNK, EMBED
# =============================


def load_and_chunk(directory, chunk_size=300, overlap=50):
    """Load text files and split them into chunks. Returns list of chunks with metadata."""

    chunks = []


    # ----
    # LOAD
    # ----

    if not os.path.exists(directory) or not os.path.isdir(directory):  # Validate whether directory exists and points to a folder
        return None
    
    
    for filename in sorted(os.listdir(directory)):

        if not filename.endswith((".txt", ".md")):
            continue

        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

        except (FileNotFoundError) as err_msg:  # Skip missing files
            print(f"Skipping {filename}: {err_msg}")
            continue

            
        # -----
        # CHUNK
        # -----

        start = 0
        i = 0
        
        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunks.append({
                "text": content[start:end].strip(),
                "source": filename,
                "chunk_index": f"{filename}_{i}",
                "chunk_id": f"{filename}_{i}",
                "chunk_size": chunk_size
            })
            start += chunk_size - overlap
            i += 1       
        

    return [chunk for chunk in chunks if chunk["text"]]  # Exclude empty chunks


# -----
# EMBED
# -----


@st.cache_resource
def get_embedding_model():
    """Return embedding model."""

    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks):
    """Embed chunks. Returns the updated chunks list."""

    model = get_embedding_model()

    chunk_texts = [chunk["text"] for chunk in chunks]

    embedded_chunks = model.encode(chunk_texts)

    for i, chunk in enumerate(embedded_chunks):
        chunks[i]["embedded_chunk"] = chunk

    return chunks


# ==============
# CHROMADB SETUP
# ==============


@st.cache_resource
def get_collection():
    """Set up a persistent ChromaDB client and retrive or create the collection."""

    client = chromadb.PersistentClient(path="./chroma_data")

    return client.get_or_create_collection(
        name="course_docs", 
        embedding_function=None,
        configuration={"hnsw": {"space": "cosine"}}
    )


# =======
# SIDEBAR
# =======


def render_sidebar():
    """Render sidebar display with Re-index button."""
    
    collection = get_collection()


    if "sources" not in st.session_state:  # Store sources in state if they have not been initialized

        metadata_response = collection.get(
            include=["metadatas"]
        )    

        sources_set = set(metadata["source"] for metadata in metadata_response["metadatas"])

        st.session_state["sources"] = sources_set
    
        
    with st.sidebar:

        st.title("📁 Document Manager")

        col_left, col_right = st.columns(2)

        with col_left:

            chunk_size = st.radio(
                "Chunk Size",
                [
                    150,
                    300,
                    500
                ],
                index=1,
                key="chunk_size"
            )

        with col_right:
        
            overlap = st.radio(
                "Chunk Overlap",
                [
                    50,
                    100
                ],
                index=0,
                key="overlap"
            )

            st.space("small")


        if st.button("🔄 Re-index Documents"):

            with st.spinner(
                "Preparing documents",
                show_time=False,
            ):
                chunks = load_and_chunk("docs", chunk_size, overlap)

            if chunks:  # If there are chunks available, embed them and add them to the collection

                chunks_with_embeddings = embed_chunks(chunks)


                existing_ids = collection.get()["ids"]

                if existing_ids:
                    collection.delete(ids=existing_ids)  # If applicable, delete old collection so as to cleanly reflect new chunk/overlap size


                collection.upsert(
                    documents=[chunk["text"] for chunk in chunks_with_embeddings],
                    embeddings=[chunk["embedded_chunk"] for chunk in chunks_with_embeddings],
                    metadatas=[{"source": chunk["source"], "chunk_index": str(chunk["chunk_index"]), "chunk_size": chunk["chunk_size"]} for chunk in chunks_with_embeddings],
                    ids=[chunk["chunk_id"] for chunk in chunks_with_embeddings],
                )            
                st.session_state["sources"] = set(chunk["source"] for chunk in chunks_with_embeddings)

                st.success(f"Indexed {len(chunks_with_embeddings)} chunks from {len(st.session_state['sources'])} files")
            
            else:  # If no chunks are available
                st.warning("No .txt or .md files found in docs/ folder")


        st.divider()
        
        st.write("Database Details:")
        
        col_left, col_right = st.columns(2)

        with col_left:       
        
            st.metric(
                "Documents (Chunks)", 
                collection.count()
            )

        with col_right:
        
            st.metric(
                "Source Files",
                len(st.session_state["sources"])
            )        
        
        st.divider()


        n_results_setting = st.slider("Number of Results to Display", 1, 10, 5, key="n_results")

        source_select = st.multiselect(
            "Search only these sources",
            sorted(st.session_state["sources"]),  # Converts set into a sorted list,
            key="source_select"
        )

        threshold = st.radio(
            "Similarity Threshold",
            [
                0.3,
                0.5,
                0.7
            ],
            index=1,
            key="threshold"
        )