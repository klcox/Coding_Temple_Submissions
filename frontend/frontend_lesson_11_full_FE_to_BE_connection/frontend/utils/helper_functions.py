import streamlit as st


def logout():
    """Log out a user. Clear session state variables and return to the Welcome screen."""

    st.session_state.clear()
    st.session_state["current_view"] = "welcome"
    st.rerun()


def handle_validation_errors(response):
    """Format validation errors from API response."""

    errors = response["error_data"]["detail"]
    
    for error in errors:
        st.toast(f"{error['field']}: {error['message']}")


def handle_api_errors(response):
    """Handle API error responses and display them to the user. If 401 or 403, log out the user."""

    if response["status_code"] in [401, 403]:
        st.toast(f"{response['error_data']['detail']} Logging out.", icon="⚠️")
        logout()

    else:
        st.toast(f"{response['error_data']['detail']}", icon="⚠️")


def validate_username(username):
    """Validate username for form input."""

    if not username.strip():
        return "Username required"

    elif len(username.strip()) < 2:
        return "Username cannot be fewer than 2 characters"

    elif len(username.strip()) > 50:
        return "Username cannot exceed 50 characters"

    return None


def validate_email(email):
    """Validate email for form input."""

    if not email.strip():
        return "Email required"

    elif len(email.strip()) < 7:
        return "Email address cannot be fewer than 7 characters"

    elif len(email.strip()) > 100:
        return "Email address cannot exceed 100 characters"

    return None


def validate_password(password, confirm_password):
    """Validate password for form input."""

    if not password:
        return "Password required"

    elif len(password) < 8:
        return "Password cannot be fewer than 8 characters"

    elif len(password) > 200:
        return "Password cannot exceed 200 characters"

    elif password != confirm_password:
        return "Passwords do not match"

    return None


def validate_task_title(title):
    """Validate the task title when creating or editing a task."""

    if not title.strip():
        return "Please enter a task title"

    elif len(title.strip()) > 200:
        return "Task title cannot exceed 200 characters"

    return None