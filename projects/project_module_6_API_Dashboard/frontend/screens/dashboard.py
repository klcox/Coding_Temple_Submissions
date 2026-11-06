import streamlit as st
from frontend.utils.helper_functions import logout, handle_validation_errors, handle_api_errors, render_header, render_pagination
from frontend.api_calls.tasks import get_all_tasks, get_task_metrics, update_task_status, delete_task
from frontend.utils.modals import edit_task_modal, add_task_modal
import pandas as pd


def render_dashboard(headers):
    """Display the main dashboard and sidebar."""

    priority_icons = {
        "urgent": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }


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
            metrics["pending_by_priority"]["urgent"] if metrics["pending_by_priority"]["urgent"] else "--"
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


    # ====
    # TABS
    # ====


    tab_main, tab_dataframe, tab_chart = st.tabs(["Main", "Raw Data per Page", "Tasks by Priority"])


    # --------
    # MAIN TAB
    # --------   
    
    
    with tab_main:

        # ................
        # TASK LIST HEADER
        # ................
        
        render_header(headers, key_prefix="main")


        st.space("medium")


        # .........
        # TASK DATA
        # .........
            

        sort_by, sort_order = st.session_state["sort_options"][st.session_state["selected_sort"]]

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
        

        # .................
        # TASK LIST DISPLAY
        # .................


        if tasks["data"]:  # If there are tasks to display

            for task in tasks["data"]:

                col_text, col_spacer, col_toggle, col_edit, col_delete = st.columns([5, 1, 1, 1, 1])

                # .........
                # TASK TEXT
                # .........
            
                with col_text:

                    display_status = "☑️" if task["completed"] else "⬜"
                    priority_icon = priority_icons[task["priority"].lower()]
                    title_styled = task['title'] if not task["completed"] else f"~~:gray[{task['title']}]~~"  # Plain if pending, grey and strikethrough if completed

                    st.markdown(f"{display_status} {priority_icon} {title_styled}")

                    if task["description"]:
                        with st.expander("*Description*"):
                            st.write(f"*{task['description']}*")   

                # .......................
                # TOGGLE COMPLETED STATUS
                # .......................            
                
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

                # ...........
                # UPDATE TASK
                # ...........

                with col_edit:

                    if st.button("Edit", key=f"edit_{task['id']}"):
                        edit_task_modal(headers, task)

                # ...........
                # DELETE TASK
                # ...........
                
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
            st.info("*No tasks yet. Click **Add Task** above to create your first task!*")


        st.divider()

        # ..........
        # PAGINATION
        # ..........        

        render_pagination(tasks, key_prefix="main")
        

    # -------------
    # DATAFRAME TAB
    # -------------


    df = pd.DataFrame(tasks["data"])  # Store tasks in a dataframe

    with tab_dataframe:

         with st.spinner(
            "Refreshing data...",
            show_time=False
        ):

            render_header(headers, key_prefix="df")

            st.space("small")


            if tasks["data"]:  # If there are tasks to display

                # Filter and standardize data

                filtered_df = df.copy()

                filtered_df = filtered_df[["title", "description", "priority", "completed", "created_at", "updated_at"]]  # Pull only these columns for display                    

                filtered_df["priority"] = filtered_df["priority"].map(priority_icons)  # Replace priority levels with the same icons in the header

                filtered_df["created_at"] = pd.to_datetime(filtered_df["created_at"], utc=True).dt.tz_convert("America/Chicago").dt.strftime("%m/%d/%Y, %I:%M %p")  # Convert to a readable format and timezone

                filtered_df["updated_at"] = pd.to_datetime(filtered_df["updated_at"], utc=True).dt.tz_convert("America/Chicago").dt.strftime("%m/%d/%Y, %I:%M %p")  # Convert to a readable format and timezone

                filtered_df.columns = filtered_df.columns.str.replace("_", " ").str.title()  # Standardize case and remove underscores
                            

                # Display the dataframe with pagination buttons

                st.dataframe(filtered_df, hide_index=True)

                render_pagination(tasks, key_prefix="df")

                st.caption("*Timestamps reflect CST*")

            else:  # If there are no tasks to display
                st.info("*No tasks yet. Click **Add Task** above to create your first task!*")


    # -------------
    # BAR CHART TAB
    # -------------


    with tab_chart:

        st.space("medium")


        if tasks["data"]:  # If there are tasks to display

            chart_df = pd.DataFrame(list(metrics["pending_by_priority"].items()), columns=["Priority", "Count"])      

            chart_df["Priority"] = chart_df["Priority"].str.capitalize()  # Standardize case
            
            
            st.bar_chart(
                chart_df,
                sort=False,
                x="Priority",
                y="Count",
                y_label="Number of Tasks",
                color="#256ca7"
            )

        else:  # If there are no tasks to display
            st.info("*No tasks yet. Click **Add Task** on the **Main** tab to create your first task!*")