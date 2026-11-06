import streamlit as st


def render_welcome():
    """Display Welcome screen."""
          
    st.markdown(
        "### Returning users, :blue[Login]. New users, :blue[Register] to create an account.", 
        text_alignment="center"
    )

    st.space("small")
    

    col_left, b_login, b_register, col_right = st.columns([2, 1, 1, 2])  # b for button

    with b_login:        
        login_button = st.button(
            "Login", 
            key="login_view",
            width="stretch"
        )

    with b_register:
        register_button = st.button(
            "Register", 
            key="register_view",
            width="stretch"
        )


    # Change view based on the button clicked

    if login_button:
        st.session_state["current_view"] = "login"
        st.rerun()

    if register_button:
        st.session_state["current_view"] = "register"
        st.rerun()