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


def update_sort(dropdown_key):
    """When the sorting selection changes, update all associated state variables for consistency across the app."""

    selected = st.session_state[dropdown_key]

    st.session_state["selected_sort"] = selected
    st.session_state["main_selected_sort"] = selected
    st.session_state["df_selected_sort"] = selected


def render_header(headers, key_prefix):
    """Display and manage sorting from the dropdown widget."""

    from frontend.utils.modals import add_task_modal  # Import here to avoid circular imports

    col_legend, col_sort, col_spacer, col_add = st.columns([2, 1, 2, 1])
    
    with col_legend:            
        
        st.write("🔴 Urgent   🟠 High   🟡 Medium   🟢 Low")


    with col_sort:        
            
        selected_sort = st.selectbox(
            "Sort by:",            
            list(st.session_state["sort_options"].keys()),  # Options for dropdown
            label_visibility="collapsed",            
            key=f"{key_prefix}_selected_sort",  # Unique widget key
            on_change=update_sort,  # When the selection changes, run this function and pass the args below
            args=(f"{key_prefix}_selected_sort",)
        )
    
    
    with col_add:

        # ..............
        # ADD TASK MODAL
        # .............. 

        if st.button("Add Task", key=f"{key_prefix}_add_task_modal"):
            add_task_modal(headers)


def validate_task_title(title):
    """Validate the task title when creating or editing a task."""

    if not title.strip():
        return "Please enter a task title"

    elif len(title.strip()) > 200:
        return "Task title cannot exceed 200 characters"

    return None


def render_pagination(tasks, key_prefix):
    """Display and manage task pagination buttons."""

    if tasks["data"]: # If there are tasks to display, also display pagination buttons

        meta = tasks["meta"]
    
        col_left, col_previous, col_page, col_next, col_right = st.columns([3, 2, 2, 2, 2])

        with col_previous:
            if st.button("← Previous", key=f"{key_prefix}_prev_page", disabled=meta["page"] <= 1):
                st.session_state["task_page"] -= 1
                st.session_state["tasks_loaded"] = False
                st.rerun()  # Reload tasks

        with col_page:
            st.write(f"Page {meta['page']} of {meta['num_pages']}")

        with col_next:
            if st.button("Next →", key=f"{key_prefix}_next_page", disabled=meta["page"] >= meta["num_pages"]):
                st.session_state["task_page"] += 1
                st.session_state["tasks_loaded"] = False
                st.rerun()  # Reload tasks        