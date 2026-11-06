import streamlit as st
from frontend.api_calls.user import get_profile
from frontend.utils.helper_functions import handle_api_errors
from frontend.utils.modals import update_profile_modal, delete_account_modal


def render_account(headers):
    """Display account management screen."""

    if st.session_state["profile"] is None:  # If there is no profile stored in state, get the profile before attempting to display

        # API Request

        with st.spinner(
            "Loading profile..",
            show_time=False
        ):                    
            get_profile_response = get_profile(headers)

        
        # Evaluate API Response
        
        if get_profile_response["success"]:  # Display username and email

            st.session_state["profile"] = get_profile_response["data"]

        else:
            handle_api_errors(get_profile_response)
            st.stop()


    # Display profile
            
    col_left, col_user, col_name, col_right = st.columns([4, 1, 1, 4])
                
    with col_user:  # User name column
        st.write("Username:")

    with col_name:
        st.write(st.session_state["username"])


    col_left, col_email, col_address, col_right = st.columns([4, 1, 1, 4])
                
    with col_email:  # Email column
        st.write("Email:")

    with col_address:
        st.write(st.session_state["profile"]["email"])

    st.space("small")


    # ======================
    # UPDATE & DELETE MODALS
    # ======================
    

    col_left, col_update, col_delete, col_right = st.columns([4, 1, 1, 4])

    with col_update:
        if st.button("Update Profile", key="update_profile"):
            update_profile_modal(headers)

    with col_delete:
        if st.button("Delete Account", key="delete_account"):
            delete_account_modal(headers)


    if st.button("← Back to Dashboard", key="back_to_dashboard_from_profile"):
        st.session_state["current_view"] = "dashboard"
        st.rerun()  # Reload to change view