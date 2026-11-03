import streamlit as st
from frontend.utils.helper_functions import (logout, handle_validation_errors, handle_api_errors, validate_username, validate_email, validate_password)
from frontend.api_calls.auth import register_user, login
from frontend.api_calls.tasks import get_all_tasks, update_task_status, delete_task
from frontend.api_calls.user import get_profile
from frontend.utils.modals import add_task_modal, update_profile_modal, delete_account_modal


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
    "tasks": None,
    "tasks_loaded": False,
    "previous_sort": None,
    "profile": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

        
# =====
# TITLE
# =====


if st.session_state["current_view"] in ["welcome", "login", "register"]:

    st.markdown(
        "# Welcome to Your :blue[Task Management App]", 
        text_alignment="center"
    )    
   
    st.space("medium")

elif st.session_state["current_view"] == "app":
    st.title(
        "Your Task Dashboard",
        text_alignment="center"
    )

    st.space("medium")

else:
    st.title(
        "Manage Your Account",
        text_alignment="center"
    )

    st.space("medium")


# ==============
# WELCOME SCREEN
# ==============


if st.session_state["current_view"] == "welcome":    
    
    st.markdown("### Returning users, :blue[Login]. New users, :blue[Register] to create an account.", text_alignment="center")

    st.space("small")

    col_left, b_login, b_register, col_right = st.columns([2, 1, 1, 2])    

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


    if login_button:
        st.session_state["current_view"] = "login"
        st.rerun()

    if register_button:
        st.session_state["current_view"] = "register"
        st.rerun()


# ============
# LOGIN SCREEN
# ============


if st.session_state["current_view"] == "login":

    col_left, col_login_form, col_right = st.columns([4, 2, 4])

    with col_login_form:

        with st.form("login_form", width="content"):

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted_login = st.form_submit_button("Login", key="login_submit", width="stretch")            

            if submitted_login:

                if not username.strip():
                    st.error("Username required")

                elif not password:
                    st.error("Password required")
                
                else:
                    with st.spinner(
                        "Connecting...",
                        show_time=False
                    ):
                    
                        token_response = login(username.strip(), password)

                    if token_response["success"]:
                        st.toast("Login successful!", icon="✅")
                        st.session_state["token_type"] = token_response["data"]["token_type"]
                        st.session_state["access_token"] = token_response["data"]["access_token"]
                        st.session_state["username"] = username.strip()
                        st.session_state["current_view"] = "app"
                        st.rerun()

                    elif token_response["status_code"] == 422:
                        handle_validation_errors(token_response)
                    
                    else:
                        st.error(f"Error: {token_response['error_data']['detail']}")

        if st.button("← Back", key="back_to_welcome_from_login"):
            st.session_state["current_view"] = "welcome"
            st.rerun()


# ===============
# REGISTER SCREEN
# ===============


if st.session_state["current_view"] == "register":

    col_left, col_register_form, col_right = st.columns([4, 2, 4])

    with col_register_form:

        with st.form("registration_form"):

            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password_login = st.text_input("Confirm New Password", type="password")
            submitted_register = st.form_submit_button("Create My Account", key="register_submit")

            st.caption(
                "All fields required.\n"
                "*Username: must be between 2 and 50 characters\n*"
                "*Email must be between 7 and 100 characters\n*"
                "*Password must be between 8 and 200 characters*"
            )

            if submitted_register:

                username_error = validate_username(username)
                email_error = validate_email(email)
                password_error = validate_password(password, confirm_password_login)

                if username_error:
                    st.error(username_error)

                elif email_error:
                    st.error(email_error)

                elif password_error:
                    st.error(password_error)


                else:
                    with st.spinner(
                        "Connecting...",
                        show_time=False
                    ):
                        user_response = register_user(username.strip(), email.strip(), password)

                    if user_response["success"]:
                        st.toast("Account creation successful!", icon="✅")
                        st.session_state["current_view"] = "login"
                        st.rerun()

                    elif user_response["status_code"] == 422:
                        handle_validation_errors(user_response)

                    else:
                        st.error(f"Error: {user_response['error_data']['detail']}")


        if st.button("← Back", key="back_to_welcome_from_register"):
            st.session_state["current_view"] = "welcome"
            st.rerun()


# ==============
# MAIN DASHBOARD
# ==============


if st.session_state["access_token"]:
    headers = {
        "Authorization": f"{st.session_state['token_type']} {st.session_state['access_token']}",
    } 



if st.session_state["current_view"] == "app": 


    # -------
    # SIDEBAR
    # -------


    with st.sidebar:
        st.subheader(f"Logged in as **{st.session_state['username']}**")
        
        st.caption("*Task Sorting Options*")

        sort_options = {
            "Priority (Highest first)": ("priority", "desc"),
            "Priority (Lowest first)": ("priority", "asc"),
            "Newest first": ("created_at", "desc"),
            "Oldest first": ("created_at", "asc"),
            "Title (A-Z)": ("title", "asc"),
            "Title (Z-A)": ("title", "desc"),
            "Completed first": ("completed", "desc"),
            "Pending first": ("completed", "asc"),
        }
        
        selected_sort = st.selectbox(
            "Sort by:", 
            list(sort_options.keys()),
            index=0
        )

        st.divider()

        if st.button("⚙️ Manage Account", key="manage_account"):
            st.session_state["current_view"] = "account"
            st.rerun()

        if st.button("🚪 Logout", key="logout"):
            logout()


    # ---------
    # TASK DATA
    # ---------
       
    
    sort_by, sort_order = sort_options[selected_sort]

    current_sort = (sort_by, sort_order)

    if st.session_state["previous_sort"] != current_sort:
        st.session_state["tasks_loaded"] = False
        st.session_state["previous_sort"] = current_sort

    if not st.session_state["tasks_loaded"]:
        with st.spinner(
            "Refreshing dashboard...",
            show_time=False
        ):
            tasks_response = get_all_tasks(headers, sort_by=sort_by, sort_order=sort_order)

        if tasks_response["success"]:            
            st.session_state["tasks"] = tasks_response["data"]
            st.session_state["tasks_loaded"] = True

        else:
            handle_api_errors(tasks_response)
            st.stop()
    
    tasks = st.session_state["tasks"]


    # -------
    # METRICS
    # -------


    m_urgent, m_pending, m_completed, m_total = st.columns(4)

    
    num_urgent = sum(1 for t in tasks["data"] if t["priority"].lower() == "urgent" and not t["completed"])    
    with m_urgent:
        st.metric(
            "Pending (Urgent)",
            num_urgent if num_urgent else "--"
        )

    num_pending = sum(1 for t in tasks["data"] if not t["completed"])
    with m_pending:
        st.metric(
            "Pending (All)",
            num_pending if num_pending else "--"
        )

    num_completed = sum(1 for t in tasks["data"] if t["completed"])
    with m_completed:
        st.metric(
            "Completed",
            num_completed if num_completed else "--"
        )

    total_tasks = len(tasks["data"])
    with m_total:
        st.metric(
            "Total Tasks",
            total_tasks if total_tasks else "--"
        )

    st.divider()


    # ---------
    # TASK LIST
    # ---------
    

    priority_icons = {
        "urgent": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }

    st.write("🔴 Urgent   🟠 High   🟡 Medium   🟢 Low")

    
    if tasks["data"]:

        for task in tasks["data"]:
            col_text, col_toggle, col_delete = st.columns([4, 1, 1])

            with col_text:
                status = "☑️" if task["completed"] else "⬜"
                priority_icon = priority_icons[task["priority"].lower()]
                title_style = task['title'] if not task["completed"] else f"~~:gray[{task['title']}]~~"

                st.markdown(f"{status} {priority_icon} {title_style}")

                if task["description"]:
                    with st.expander("*Description*"):
                        st.write(f"*{task['description']}*")                

            with col_toggle:
                label = "Undo" if task["completed"] else "Complete"
                if st.button(label, key=f"toggle_patch_{task['id']}"):

                    status = False if task["completed"] else True

                    with st.spinner(
                        "Updating task...",
                        show_time=False
                    ):
                        update_task_response = update_task_status(headers, task["id"], status)

                        if update_task_response["success"]:
                            st.toast("Task updated successfully!", icon="✅")
                            st.session_state["tasks_loaded"] = False
                            st.rerun()

                        elif update_task_response["status_code"] == 422:
                            handle_validation_errors(update_task_response)

                        else:
                            handle_api_errors(update_task_response)

            with col_delete:                
                if st.button("Delete", key=f"toggle_delete_{task['id']}"):

                    with st.spinner(
                        "Deleting task...",
                        show_time=False
                    ):                    
                        delete_task_response = delete_task(headers, task["id"])

                        if delete_task_response["success"]:
                            st.toast("Task deleted successfully!", icon="✅")
                            st.session_state["tasks_loaded"] = False
                            st.rerun()

                        else:
                            handle_api_errors(delete_task_response)

    else:
        st.info("*No tasks yet. Click **Add Task** below to create your first task!*")

    st.divider()


    # --------------
    # ADD TASK MODAL
    # --------------
   

    if st.button("Add Task", key="add_task_modal"):
        add_task_modal(headers)


# =========================
# ACCOUNT MANAGEMENT SCREEN
# =========================


if st.session_state["current_view"] == "account":    

    if st.session_state["profile"] is None:

        with st.spinner(
            "Loading profile..",
            show_time=False
        ):                    
            get_profile_response = get_profile(headers)

        if get_profile_response["success"]:

            st.session_state["profile"] = get_profile_response["data"]

            col_user, col_name = st.columns(2)
            
            with col_user:
                st.write("Username:")
        
            with col_name:
                st.write(st.session_state["username"])


            col_email, col_address = st.columns(2)
                        
            with col_email:
                st.write("Email:")
        
            with col_address:
                st.write(st.session_state["profile"]["email"])

        else:
            handle_api_errors(get_profile_response)
            st.stop()
            

    # --------------------
    # UPDATE/DELETE MODALS
    # --------------------

            
    if st.button("Update Profile", key="update_profile"):
        update_profile_modal(headers)     
    
    if st.button("Delete Account", key="delete_account"):
        delete_account_modal(headers)    