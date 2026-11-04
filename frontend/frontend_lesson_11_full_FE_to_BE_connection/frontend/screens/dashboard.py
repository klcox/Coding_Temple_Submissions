import streamlit as st
from frontend.utils.helper_functions import logout, handle_validation_errors, handle_api_errors
from frontend.api_calls.tasks import get_all_tasks, get_task_metrics, update_task_status, delete_task
from frontend.utils.modals import edit_task_modal, add_task_modal


def render_dashboard(headers):
    """Display the main dashboard and sidebar."""
    

    # =======
    # SIDEBAR
    # =======


    with st.sidebar:
        st.subheader(f"Logged in as :blue[{st.session_state['username']}]")

        st.space("small")       

        if st.button("⚙️ Manage Account", key="manage_account"):
            st.session_state["current_view"] = "account"
            st.rerun()  # Reload to change view        
        
        st.divider()

        if st.button("🚪 Logout", key="logout"):
            st.toast("Log out successful!", icon="✅")
            logout()
   

    # ============
    # METRICS DATA
    # ============


    if not st.session_state["metrics_loaded"]:

        # API Request
        
        with st.spinner(
            "Refreshing metrics...",
            show_time=False
        ):
            metrics_response = get_task_metrics(headers)
        
        
        # Evaluate API response

        if metrics_response["success"]:  # Update state variables            
            st.session_state["metrics_loaded"] = True        
            st.session_state["metrics"] = metrics_response["data"] 
                                                   
        else:
            handle_api_errors(metrics_response)
            st.stop()    
   
    metrics = st.session_state["metrics"]


    # ===============
    # METRICS DISPLAY
    # ===============
    

    m_urgent, m_pending, m_completed, m_total = st.columns(4)  # m for metric    
        
    with m_urgent:
        st.metric(
            "Pending (Urgent)",
            metrics["urgent"] if metrics["urgent"] else "--"
        )

    with m_pending:
        st.metric(
            "Pending (All)",
            metrics["pending"] if metrics["pending"] else "--"
        )

    with m_completed:
        st.metric(
            "Completed",
            metrics["completed"] if metrics["completed"] else "--"
        )

    with m_total:
        st.metric(
            "Total Tasks",
            metrics["total"] if metrics["total"] else "--"
        )

    st.divider()


    # ================
    # TASK LIST HEADER
    # ================
    

    col_legend, col_sort, col_spacer, col_add = st.columns([2, 1, 2, 1])

    with col_legend:

        priority_icons = {
            "urgent": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }
        
        st.write("🔴 Urgent   🟠 High   🟡 Medium   🟢 Low")


    with col_sort:

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
            label_visibility="collapsed",
            index=0  # Default to sorting by priority, highest first (matches backend)
        )
     
    
    with col_add:

        # --------------
        # ADD TASK MODAL
        # -------------- 

        if st.button("Add Task", key="add_task_modal"):
            add_task_modal(headers)


    st.space("medium")


    # =========
    # TASK DATA
    # =========
        

    sort_by, sort_order = sort_options[selected_sort]

    current_sort = (sort_by, sort_order)

    if st.session_state["previous_sort"] != current_sort:
        st.session_state["tasks_loaded"] = False
        st.session_state["task_page"] = 1
        st.session_state["previous_sort"] = current_sort

    if not st.session_state["tasks_loaded"]:  # If there is a change in sorting preference or to the tasks themselves, reload the tasks
        
        # API Request

        with st.spinner(
            "Refreshing dashboard...",
            show_time=False
        ):
            tasks_response = get_all_tasks(
                headers, 
                sort_by=sort_by, 
                sort_order=sort_order,
                page=st.session_state["task_page"],
                limit=st.session_state["task_limit"]
            )
       
        
        # Evaluate API responses

        if tasks_response["success"]:  # Update state variables
            st.session_state["tasks"] = tasks_response["data"]
            st.session_state["tasks_loaded"] = True       
                                       
        elif tasks_response["status_code"] == 400:  # If the requested page exceeds what is returned (e.g. after deleting a task), reverts to a previous page that contains data or returns to page 1
            if st.session_state["task_page"] > 1:
                st.session_state["task_page"] -= 1

            else:
                st.session_state["task_page"] = 1

            st.session_state["tasks_loaded"] = False
            st.rerun()  # Reload tasks
                            
        else:
            handle_api_errors(tasks_response)            
            st.stop()
       
    tasks = st.session_state["tasks"]    
    meta = st.session_state["tasks"]["meta"]
    

    # =================
    # TASK LIST DISPLAY
    # =================


    if tasks["data"]:  # If there are tasks to display

        for task in tasks["data"]:

            col_text, col_spacer, col_toggle, col_edit, col_delete = st.columns([5, 1, 1, 1, 1])

            # ---------
            # TASK TEXT
            # ---------
        
            with col_text:

                display_status = "☑️" if task["completed"] else "⬜"
                priority_icon = priority_icons[task["priority"].lower()]
                title_styled = task['title'] if not task["completed"] else f"~~:gray[{task['title']}]~~"  # Plain if pending, grey and strikethrough if completed

                st.markdown(f"{display_status} {priority_icon} {title_styled}")

                if task["description"]:
                    with st.expander("*Description*"):
                        st.write(f"*{task['description']}*")   

            # -----------------------
            # TOGGLE COMPLETED STATUS
            # -----------------------            
            
            with col_toggle:

                label = "Undo" if task["completed"] else "Mark Complete"
                if st.button(label, key=f"toggle_patch_{task['id']}"):

                    completed_status = False if task["completed"] else True  # Set opposite status

                    # API Request

                    with st.spinner(
                        "Updating task...",
                        show_time=False
                    ):
                        update_task_response = update_task_status(headers, task["id"], completed_status)


                    # Evaluate API response

                    if update_task_response["success"]:
                        st.toast("Task updated successfully!", icon="✅")
                        st.session_state["metrics_loaded"] = False
                        st.session_state["tasks_loaded"] = False
                        st.rerun()  # Reload tasks

                    elif update_task_response["status_code"] == 422:
                        handle_validation_errors(update_task_response)

                    else:
                        handle_api_errors(update_task_response)

            # -----------
            # UPDATE TASK
            # -----------

            with col_edit:

                if st.button("Edit", key=f"edit_{task['id']}"):
                    edit_task_modal(headers, task)

            # -----------
            # DELETE TASK
            # -----------
            
            with col_delete:

                if st.button("Delete", key=f"delete_{task['id']}", type="tertiary"):
                    
                    # API Request

                    with st.spinner(
                        "Deleting task...",
                        show_time=False
                    ):                    
                        delete_task_response = delete_task(headers, task["id"])

                    
                    # Evaluate API response

                    if delete_task_response["success"]:
                        st.toast("Task deleted successfully!", icon="✅")
                        st.session_state["metrics_loaded"] = False
                        st.session_state["tasks_loaded"] = False
                        st.rerun()  # Reload tasks

                    else:
                        handle_api_errors(delete_task_response)

    else:  # If there are no tasks to display
        st.info("*No tasks yet. Click **Add Task** below to create your first task!*")


    st.divider()


    # ==========
    # PAGINATION
    # ==========


    if tasks["data"]: # If there are tasks to display, also display pagination buttons

        col_left, col_previous, col_page, col_next, col_right = st.columns([3, 2, 2, 2, 2])

        with col_previous:
            if st.button("← Previous", key="prev_page", disabled=meta["page"] <= 1):
                st.session_state["task_page"] -= 1
                st.session_state["tasks_loaded"] = False
                st.rerun()  # Reload tasks

        with col_page:
            st.write(f"Page {meta['page']} of {meta['num_pages']}")

        with col_next:
            if st.button("Next →", key="next_page", disabled=meta["page"] >= meta["num_pages"]):
                st.session_state["task_page"] += 1
                st.session_state["tasks_loaded"] = False
                st.rerun()  # Reload tasks