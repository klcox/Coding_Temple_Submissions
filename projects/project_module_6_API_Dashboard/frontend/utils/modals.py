import streamlit as st
from frontend.api_calls.tasks import update_task_details, add_new_task
from frontend.api_calls.user import update_profile, deactivate_account
from frontend.utils.helper_functions import logout, handle_validation_errors, handle_api_errors, validate_task_title, validate_email, validate_password


@st.dialog("Edit Task Details")
def edit_task_modal(headers: dict, task: dict):
    """Modal for editing an existing task. Runs when the 'Edit' button is clicked from the Main Dashboard."""

    col_existing_task, col_edits = st.columns(2)

    with col_existing_task:  # Display current task details        

        st.markdown(f"**:blue[Title]**")
        st.write(task["title"])

        st.write("")

        st.markdown(f"**:blue[Description]**")
        st.write(task["description"] if task["description"] else "N/A")

        st.write("")

        st.markdown(f"**:blue[Priority]**")
        st.write(task["priority"].capitalize())


    with col_edits:

        with st.form("edit_task_form"):
        
            edited_title = st.text_input("New Title")
            st.caption("*If included, title must be between 1 and 200 characters.*")

            edited_desc = st.text_area("New Description")
            st.caption("*If included, description must be between 1 and 2000 characters.*")

            edited_priority = st.selectbox("New Priority", ["Low", "Medium", "High", "Urgent"], index=None)
            submitted_edits = st.form_submit_button("Update Task", key="edit_task_submit", width="stretch")
                       
                       
            if submitted_edits:  # If submit button is clicked

                # Validation
                
                title_error = validate_task_title(edited_title) if edited_title else None  # Only validate title if provided              
                
                if title_error:
                    st.error(title_error)

                elif edited_desc.strip() and len(edited_desc.strip()) > 2000:  # Only validate desc if provided
                    st.error("Description cannot exceed 2000 characters.")

                elif not edited_title and not edited_desc and not edited_priority:
                    st.warning("Please provide at least one update.")


                # API Request
                
                else:
                    task_updates = {}  # Only include submitted fields
                    
                    if edited_title:
                        task_updates["title"] = edited_title.strip()
                    
                    if edited_desc:
                        task_updates["description"] = edited_desc.strip()

                    if edited_priority:
                        task_updates["priority"] = edited_priority.lower()                    
                    
    
                    with st.spinner(
                        "Updating task...",
                        show_time=False
                    ):                
                        edit_task_response = update_task_details(headers, task["id"], task_updates)
    
    
                    # Evaluate API Response
    
                    if edit_task_response["success"]:
                        st.toast("Task updated successfully!", icon="✅")
                        st.session_state["metrics_loaded"] = False
                        st.session_state["tasks_loaded"] = False             
                        st.rerun()  # Reload tasks
    
                    elif edit_task_response["status_code"] == 422:
                        handle_validation_errors(edit_task_response)
    
                    else:
                        handle_api_errors(edit_task_response)
                

@st.dialog("New Task Details")
def add_task_modal(headers: dict):
    """Modal for adding a new task. Runs when the 'Add Task' button is clicked from the Main Dashboard."""

    with st.form("add_task_form"):

        new_title = st.text_input("Title")
        st.caption("*Title is **required** and must be between 1 and 200 characters.*")

        new_desc = st.text_area("Description (Optional)")
        st.caption("*If included, description must be between 1 and 2000 characters.*")

        new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"], index=1)
        submitted_task = st.form_submit_button("Add Task", key="add_task_submit", width="stretch")
       
        
        if submitted_task:  # If submit button is clicked

            # Validation

            title_error = validate_task_title(new_title)

            if title_error:
                st.error(title_error)

            elif new_desc.strip() and len(new_desc.strip()) > 2000:  # Only validate desc if provided
                st.error("Description cannot exceed 2000 characters.")


            # API Request

            else:
                new_task = {
                    "title": new_title.strip(),
                    "description": new_desc.strip() or None,  # Prevents submitting an empty string
                    "priority": new_priority.lower()
                }

                with st.spinner(
                    "Adding task...",
                    show_time=False
                ):                
                    add_task_response = add_new_task(headers, new_task)


                # Evaluate API Response

                if add_task_response["success"]:
                    st.toast("Task added successfully!", icon="✅")
                    st.session_state["metrics_loaded"] = False
                    st.session_state["tasks_loaded"] = False             
                    st.rerun()  # Reload tasks

                elif add_task_response["status_code"] == 422:
                    handle_validation_errors(add_task_response)

                else:
                    handle_api_errors(add_task_response)


@st.dialog("Update Your Account")
def update_profile_modal(headers: dict):
    """Modal to update a user's email or password. Runs when the 'Update Profile' button is clicked from the Account Management screen."""

    with st.form("update_profile_form"):

        st.caption("You may update your email address, password, or both.")

        new_email = st.text_input("Email", type="email", placeholder="")
        st.caption("*If included, email must be between 7 and 100 characters.*")

        new_password = st.text_input("Password", type="password")
        st.caption("*If included, password must be between 8 and 200 characters.*")

        confirm_password_update = st.text_input("Confirm New Password", type="password")
        submitted_profile = st.form_submit_button("Submit", key="update_profile_submit", width="stretch")
    
        
        if submitted_profile:  # If submit button is clicked

            # Validation

            email_error = validate_email(new_email) if new_email else None  # Only validate email if provided

            password_error = validate_password(new_password, confirm_password_update) if new_password else None  # Only validate password if provided
            
            if email_error:
                st.error(email_error)

            elif password_error:
                st.error(password_error)

            elif not new_email and not new_password:  # If both fields are empty
                st.warning("Please provide at least one update.")


            # API Request

            else:
                profile_updates = {}  # Only include submitted fields

                if new_email:
                    profile_updates["email"] = new_email.strip()
                
                if new_password:
                    profile_updates["password"] = new_password  


                with st.spinner(
                    "Updating profile...",
                    show_time=False
                ):                
                    update_profile_response = update_profile(headers, profile_updates)

                
                # Evaluate API Response
                
                if update_profile_response["success"]:
                    st.toast("Profile updated successfully!", icon="✅")
                    st.session_state["profile"] = update_profile_response["data"]                                      
                    st.rerun()  # Reload profile display

                elif update_profile_response["status_code"] == 422:
                    handle_validation_errors(update_profile_response)

                else:
                    handle_api_errors(update_profile_response) 


@st.dialog("❗ Delete Account")
def delete_account_modal(headers: dict):
    """Modal to confirm a user's request to delete their account. Runs when the 'Delete Account' button is clicked from the Account Management screen."""
    
    st.error(
        "Are you sure you want to delete your account?  \n"
        "**This action cannot be undone.**"
    )

    col_cancel, col_delete = st.columns(2)

    with col_cancel:
        if st.button("Cancel", key="cancel_delete", width="stretch"):
            st.rerun()  # Close dialog box and refresh the Account Management screen

    with col_delete:
        if st.button("Delete Account", type="primary", key="delete_account_submit", width="stretch"):

            # API Request
            
            with st.spinner(
                "Deleting account...",
                show_time=False
            ):
                deactivate_response = deactivate_account(headers)
                

            # Evaluate API Response
            
            if deactivate_response["success"]:
                st.toast("Account deleted successfully!", icon="✅")
                logout()

            else:
                handle_api_errors(deactivate_response)