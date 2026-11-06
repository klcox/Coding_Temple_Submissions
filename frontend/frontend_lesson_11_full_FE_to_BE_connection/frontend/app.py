import streamlit as st
from frontend.screens.welcome import render_welcome
from frontend.screens.login import render_login
from frontend.screens.register import render_register
from frontend.screens.account import render_account
from frontend.screens.dashboard import render_dashboard


# ===========
# PAGE CONFIG
# ===========


st.set_page_config(
    page_title="Task Management App",
    page_icon="📝",
    layout="wide"   
)


# ===============
# STATE VARIABLES
# ===============


defaults = {
    "token_type": None,
    "access_token": None,
    "username": None,
    "current_view": "welcome",
    "metrics_loaded": None,
    "metrics": None,    
    "tasks_loaded": False,
    "tasks": None,
    "task_page": 1,
    "task_limit": 10,
    "previous_sort": None,
    "profile": None
}

for key, value in defaults.items():  # Initialize only the values that are not already established in state
    if key not in st.session_state:
        st.session_state[key] = value


if st.session_state["access_token"]:  # If the user is logged in, store their auth headers in state for reusability
    headers = {
        "Authorization": f"{st.session_state['token_type']} {st.session_state['access_token']}",
    }
    
        
# =====
# TITLE
# =====


if st.session_state["current_view"] in ["welcome", "login", "register"]:

    st.markdown(
        "# Welcome to Your :blue[Task Management App]", 
        text_alignment="center"
    )    
   
elif st.session_state["current_view"] == "dashboard":
    st.title(
        "Your Task Dashboard",
        text_alignment="center"
    )

else:
    st.title(
        "Manage Your Account",
        text_alignment="center"
    )

st.space("medium")


# ==========
# NAVIGATION
# ==========


if st.session_state["current_view"] == "welcome":
    render_welcome()


if st.session_state["current_view"] == "login":
    render_login()
    

if st.session_state["current_view"] == "register":
    render_register()
    

if st.session_state["current_view"] == "account":
    render_account(headers)


if st.session_state["current_view"] == "dashboard": 
    render_dashboard(headers)