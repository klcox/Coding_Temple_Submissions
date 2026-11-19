import streamlit as st
from ingest import get_embedding_model, get_collection


def render_interface():
    """Render the main display interface with search bar and results."""    

    st.title("🔍 Semantic Search")

    st.write("Search course documents by meaning rather than keywords.")

    st.space("small")
    

    query = st.text_input("Enter your search query", placeholder="What is Streamlit?")
    
    collection = get_collection()

    model = get_embedding_model()    
    
    source_select = st.session_state["source_select"]
    n_results_setting = st.session_state["n_results"]
    threshold = st.session_state["threshold"]


    if not query and collection.count() > 0:  # If the user has not entered a query and there are docs in the collection
        st.info("👆 Enter a query to search the collection.")


    elif query and collection.count() > 0:  # If the user has entered a query and there are docs in the collection

        query_embedding = model.encode(query)
        
        
        if len(source_select) >= 2:    
            source_select_dicts = [{"source": selection} for selection in source_select]
            source_select_filter = {"$or": source_select_dicts}

        elif len(source_select) == 1:
            source_select_filter = {"source": source_select[0]}

        else:
            source_select_filter = None
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results_setting, collection.count()),
            where=source_select_filter
        )


        st.space("small")

        
        if not results["documents"][0]:  # If the collection query did not yield any matches
            st.info("No results found. Try adjusting your query or the selected sources.")
        
        else:  # If the collection query did yield matches
            st.subheader(f"Top {len(results['documents'][0])} Results")   
            st.caption(f"*Out of {collection.count()} total database documents*") 

            st.write("Result Relevance: 🟢 High  🟡 Medium  🔴 Low")

            st.space("small")
            

            num_displayed_docs = 0

            for i in range(len(results['documents'][0])):

                doc = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]

                if distance > threshold:  # Skip displaying results outside of the designated threshold
                    continue

                # Color-code by overall relevance
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

                    num_displayed_docs += 1

            if num_displayed_docs == 0:  # If no results are displayed due to threshold requirements
                st.info("No results found. Try adjusting your query, the selected sources, and/or the threshold.")

    elif collection.count() == 0:  # If there are no docs in the collection
        st.info("👈 Click 'Re-index Documents' in the sidebar to load your documents first.")