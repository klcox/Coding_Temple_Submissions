import streamlit as st
from frontend.api_calls.tasks import add_new_task
from frontend.api_calls.user import update_profile, deactivate_account
from frontend.utils.helper_functions import logout, handle_validation_errors, handle_api_errors, validate_task_title, validate_email, validate_password


@st.dialog("Task Details")
def add_task_modal(headers):

    with st.form("add_task_form"):

        new_title = st.text_input("Title:")
        new_desc = st.text_area("Description (Optional):")
        new_priority = st.selectbox("Priority:", ["Low", "Medium", "High", "Urgent"])
        submitted_task = st.form_submit_button("Add Task", key="add_task_submit", width="stretch")

        st.caption(
            "*Title is required\n*"
            "*Title must be between 1 and 200 characters*\n"
            "*If included, descriptions must be between 1 and 2000 characters\n*"                
        )
        
        if submitted_task:

            title_error = validate_task_title(new_title)

            if title_error:
                st.warning(title_error)

            elif new_desc.strip() and len(new_desc.strip()) > 2000:
                st.warning("Description cannot exceed 2000 characters.")

            else:
                new_task = {
                    "title": new_title.strip(),
                    "description": new_desc.strip() or None,
                    "priority": new_priority.lower()
                }

                with st.spinner(
                    "Adding task...",
                    show_time=False
                ):                
                    add_task_response = add_new_task(headers, new_task)

                    if add_task_response["success"]:
                        st.toast("Task added successfully!", icon="✅")
                        st.session_state["tasks_loaded"] = False             
                        st.rerun()

                    elif add_task_response["status_code"] == 422:
                        handle_validation_errors(add_task_response)

                    else:
                        handle_api_errors(add_task_response)


@st.dialog("Update Your Email Address and/or Password")
def update_profile_modal(headers):

    with st.form("update_profile_form"):

        new_email = st.text_input("Email:")
        new_password = st.text_input("Password:", type="password")
        confirm_password_update = st.text_input("Confirm New Password", type="password")
        subumitted_profile = st.form_submit_button("Submit", key="update_profile_submit", width="stretch")

        st.caption(           
            "*Email must be between 7 and 100 characters\n*"
            "*Password must be between 8 and 200 characters*"
        )
        
        if subumitted_profile:                

            email_error = validate_email(new_email) if new_email else None

            password_error = validate_password(new_password, confirm_password_update) if new_password else None
            
            if email_error:
                st.warning(email_error)

            elif password_error:
                st.warning(password_error)

            elif not new_email and not new_password:
                st.warning("Please provide at least one update.")

            else:
                profile_updates = {}

                if new_email:
                    profile_updates["email"] = new_email.strip()
                
                if new_password:
                    profile_updates["password"] = new_password                               

                with st.spinner(
                    "Updating profile...",
                    show_time=False
                ):                
                    update_profile_response = update_profile(headers, profile_updates)

                    if update_profile_response["success"]:
                        st.toast("Profile updated successfully!", icon="✅")
                        st.session_state["profile"] = update_profile_response["data"]                                      
                        st.rerun()

                    elif update_profile_response["status_code"] == 422:
                        handle_validation_errors(update_profile_response)

                    else:
                        handle_api_errors(update_profile_response) 


@st.dialog("Delete Account")
def delete_account_modal(headers):
    
    st.warning(
        "Are you sure you want to delete your account?\n"
        "**This action cannot be undone.**"
    )

    col_cancel, col_delete = st.columns(2)

    with col_cancel:
        if st.button("Cancel", key="cancel_delete", width="stretch"):
            st.rerun()

    with col_delete:
        if st.button("Delete Account", type="primary", key="delete_account_submit", width="stretch"):

            with st.spinner(
                "Deleting account...",
                show_time=False
            ):
                deactivate_response = deactivate_account(headers)

            if deactivate_response["success"]:
                st.toast("Account deleted successfully!", icon="✅")
                logout()

            else:
                handle_api_errors(deactivate_response)