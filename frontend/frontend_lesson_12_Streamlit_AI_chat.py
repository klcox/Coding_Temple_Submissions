import streamlit as st
import time


# ===========
# PAGE CONFIG
# ===========


st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="centered"
)


# ===============
# STATE VARIABLES
# ===============


if "messages" not in st.session_state:
    st.session_state["messages"] = []


# =======
# SIDEBAR
# =======


with st.sidebar:

    st.header("Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant for students learning AI engineering.",
        help="This sets the AI's personality and behavior."
    )

    st.caption("*System prompt to be used with real AI integration only.*")


    contexts = []

    context_python = st.checkbox("Include Python expertise")

    if context_python:
        contexts.append("Python")

    
    context_web = st.checkbox("Include web development context")

    if context_web:
        contexts.append("Web Development")

    
    context_ml = st.checkbox("Include AI/ML context")

    if context_ml:
        contexts.append("AI/ML")
    
    
    st.divider()


    if st.button("Clear Chat", key="clear_chat"):
        st.session_state["messages"] = []
        st.rerun()

    
# =======================
# MOCK RESPONSE GENERATOR
# =======================


def mock_stream(prompt, contexts):
    """Fake streaming response for demo purposes."""

    # Format context string for response

    if len(contexts) >= 3:
        context_str = ", ".join(contexts[:-1]) + ", and " + contexts[-1]
    
    elif len(contexts) == 2:
        context_str = "".join(contexts[:-1]) + " and " + contexts[-1]

    elif len(contexts) == 1:
        context_str = contexts[0]

    else:
        context_str = "general knowledge"


    response = f"Based on my {context_str} expertise, here's my take on '{prompt[:50]}': *[placeholder for real AI response in production]*"    
    
    for word in response.split():  # Split the response by word and generate one at a time to simulate streaming from a real AI model
        yield word + " "
        time.sleep(0.3)


# ==============
# MAIN INTERFACE
# ==============


st.title("💬 AI Chat", text_alignment="center")

st.space("small")


# Reload chat history

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Handle new user input

if prompt := st.chat_input("Ask me anything..."):  # If the user enters a new prompt

    st.session_state["messages"].append({"role": "user", "content": prompt})  # Add user message to chat history
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking...",
            show_time=False
        ):
            response = st.write_stream(mock_stream(prompt, contexts))
            
    st.session_state["messages"].append({"role": "assistant", "content": response})  # Add AI model message to chat history