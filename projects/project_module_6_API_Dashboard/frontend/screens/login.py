import streamlit as st
from frontend.api_calls.auth import login
from frontend.utils.helper_functions import handle_validation_errors


def render_login():
    """Display login screen."""

    col_left, col_login_form, col_right = st.columns([4, 2, 4])

    with col_login_form:

        with st.form("login_form", width="content"):

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted_login = st.form_submit_button("Login", key="login_submit", width="stretch")            

            if submitted_login:  # If submit button is clicked

                # Validation

                if not username.strip():
                    st.error("Username required")

                elif not password:
                    st.error("Password required")


                # API Request  
                
                else:
                    with st.spinner(
                        "Connecting...",
                        show_time=False
                    ):
                    
                        token_response = login(username.strip(), password)


                    # Evaluate API response
                    
                    if token_response["success"]:
                        st.toast("Login successful!", icon="✅")


                        # Update state variables

                        st.session_state["token_type"] = token_response["data"]["token_type"]
                        st.session_state["access_token"] = token_response["data"]["access_token"]
                        st.session_state["username"] = username.strip()
                        st.session_state["current_view"] = "dashboard"


                        st.rerun()  # Reload to change view

                    elif token_response["status_code"] == 422:
                        handle_validation_errors(token_response)
                    
                    else:
                        st.error(f"Error: {token_response['error_data']['detail']}")


        if st.button("← Back", key="back_to_welcome_from_login"):
            st.session_state["current_view"] = "welcome"
            st.rerun()  # Reload to change view