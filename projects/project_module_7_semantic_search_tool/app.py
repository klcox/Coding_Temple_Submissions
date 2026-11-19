import streamlit as st
from ingest import render_sidebar
from search import render_interface


# ===========
# PAGE CONFIG
# ===========


st.set_page_config(
    page_title="Semantic Search", 
    page_icon="🔍", 
    layout="wide"
)


# =======
# SIDEBAR
# =======


render_sidebar()


# ==============
# MAIN INTERFACE
# ==============


render_interface()