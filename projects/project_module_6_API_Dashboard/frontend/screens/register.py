import streamlit as st
from frontend.utils.helper_functions import validate_username, validate_email, validate_password, handle_validation_errors
from frontend.api_calls.auth import register_user

def render_register():
    """Display registration screen."""

    col_left, col_register_form, col_right = st.columns([4, 2, 4])

    with col_register_form:

        with st.form("registration_form"):

            username = st.text_input("Username")
            st.caption("*Username must be between 2 and 50 characters.*")

            email = st.text_input("Email", type="email", placeholder="")
            st.caption("*Email must be between 7 and 100 characters.*")

            password = st.text_input("Password", type="password")
            st.caption("*Password must be between 8 and 200 characters.*")

            confirm_password_register = st.text_input("Confirm Password", type="password")
            submitted_register = st.form_submit_button("Create My Account", key="register_submit", width="stretch")
            

            if submitted_register:  # If submit button is clicked

                # Validation

                username_error = validate_username(username)
                email_error = validate_email(email)
                password_error = validate_password(password, confirm_password_register)                

                if username_error:
                    st.error(username_error)

                elif email_error:
                    st.error(email_error)

                elif password_error:
                    st.error(password_error)


                # API Request

                else:
                    with st.spinner(
                        "Connecting...",
                        show_time=False
                    ):
                        user_response = register_user(username.strip(), email.strip(), password)


                    # Evaluate API response
                    
                    if user_response["success"]:
                        st.toast("Account creation successful!", icon="✅")
                        st.session_state["current_view"] = "login"
                        st.rerun()  # Reload to change view

                    elif user_response["status_code"] == 422:
                        handle_validation_errors(user_response)

                    else:
                        st.error(f"Error: {user_response['error_data']['detail']}")


        if st.button("← Back", key="back_to_welcome_from_register"):
            st.session_state["current_view"] = "welcome"
            st.rerun()  # Reload to change view