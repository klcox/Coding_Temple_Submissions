import streamlit as st
import requests
import pandas as pd


# ======
# CONFIG
# ======


st.set_page_config(
    page_title="Data Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========
# PAGE TITLE
# ==========


st.title("Data Explorer", text_alignment="center")
st.caption("User data from JSONPlaceholder API", text_alignment="center")


# ===========
# CACHED DATA
# ===========


@st.cache_data(ttl=300)
def fetch_users():
    """Gets all users from JSONPlaceholder API. Returns the response as JSON."""

    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)

        response.raise_for_status()  # If the response status code is 4XX or 5XX (an error), this method raises an HTTPError

    except requests.Timeout:
        print("Error: The request timed out. Please try again.")
        st.error("Error: The request timed out. Please try again.")
        st.stop()        

    except requests.RequestException as err_msg:
        print(f"\nRequest failed: {err_msg}") 
        st.error(f"Request failed: {err_msg}")
        st.stop() 

    return response.json()

with st.spinner(
    "Loading users...",
    show_time=False
):
    users = fetch_users()


# =======
# METRICS
# =======


m_total_users, m_unique_cities, m_unique_companies = st.columns(3)

with m_total_users:
    st.metric(
        "Total Users",
        len(users)
    )

with m_unique_cities:
    st.metric(
        "Unique Cities",
        len({user["address"]["city"] for user in users})
    )

with m_unique_companies:
    st.metric(
        "Unique Companies",
        len({user["company"]["name"] for user in users})
    )


# =======
# SIDEBAR
# =======


with st.sidebar:
    st.header("⚙️ Controls")
    st.caption("*For DataFrame Tab Only*")

    name_filter = st.text_input("User Name Contains").strip()

    sort_by = st.selectbox(
        "Sort By",
        [
            "Name",
            "Email",
            "City",
            "Company"
        ],
        index=None,
    )
    st.caption("*Default settings sort by User ID*")


# ===================
# TABBED DATA DISPLAY
# ===================


tab_dataframe, tab_bar = st.tabs([
    "Interactive DataFrame",
    "Bar Chart"
])


with tab_dataframe:
    data_rows = [
        {
            "User ID": user["id"],        
            "Name": user["name"],
            "Email": user["email"],
            "City": user["address"]["city"],
            "Company": user["company"]["name"]
        }
        for user in users
    ]

    df = pd.DataFrame(data_rows)

    filtered_df = df.copy()

    
    st.subheader("Raw User Data")

    if name_filter:        

        filtered_df = filtered_df[filtered_df["Name"].str.contains(
            name_filter,
            case=False,  # Makes the filtering case-insensitive
            na=False  # Prevents missing value errors
        )]
       
    if sort_by:
        filtered_df = filtered_df.sort_values(sort_by, ascending=True)

    st.caption(f"Showing {len(filtered_df)} of {len(df)} Users")
    
    st.dataframe(
        filtered_df,
        hide_index=True
    )               


with tab_bar:

    chart_data = df.groupby("City").size().reset_index(name="Number of Users")

    st.subheader("Number of Users per City") 

    st.bar_chart(
        chart_data,
        x="City",
        y="Number of Users"
    )