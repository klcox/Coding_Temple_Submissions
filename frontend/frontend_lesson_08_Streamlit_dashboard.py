import streamlit as st
import pandas as pd


# ======
# CONFIG
# ======


st.set_page_config(
    page_title="Bootcamp Dashboard",
    page_icon="📊",
    layout="wide"  # Uses full browser width
)


# ===================
# DATA & CALCULATIONS
# ===================


MODULES = [
    {
        "number": "A",
        "title": "Pre-Work: Logical & Critical Thinking",
        "num_lessons": 5
    },
    {
        "number": "B",
        "title": "Pre-Work: Computer Literacy & Terminal",
        "num_lessons": 6
    },
    {
        "number": "C",
        "title": "Pre-Work: Python Fundamentals",
        "num_lessons": 12
    },
    {
        "number": "1",
        "title": "AI Foundations",
        "num_lessons": 8
    },
    {
        "number": "2",
        "title": "Advanced Python & Data Handling",
        "num_lessons": 9
    },
    {
        "number": "3",
        "title": "Databases & SQLAlchemy",
        "num_lessons": 10
    },
    {
        "number": "4",
        "title": "REST API Fundamentals",
        "num_lessons": 11
    },
    {
        "number": "5",
        "title": "FastAPI Development",
        "num_lessons": 13
    },
    {
        "number": "6",
        "title": "Web Essentials & Streamlit",
        "num_lessons": 13
    },
    {
        "number": "7",
        "title": "Applied AI - Embeddings & Retrieval",
        "num_lessons": 11
    },
    {
        "number": "8",
        "title": "RAG Intro & Docker Deployment",
        "num_lessons": 13
    },
    {
        "number": "9",
        "title": "Capstone",
        "num_lessons": 1
    },
]

lessons_total = sum([module["num_lessons"] for module in MODULES ])

LESSONS_COMPLETED_BY_MONTH = {
    "June": 11,
    "July": 22,
    "August": 15,
    "September": 16,
    "October": 17,
    "November": 0,
    "December": 0
}

lessons_completed = sum(LESSONS_COMPLETED_BY_MONTH.values())

lessons_to_complete = lessons_total - lessons_completed


last_month_completed = lessons_completed - LESSONS_COMPLETED_BY_MONTH["October"]
last_month_completion_rate = last_month_completed/lessons_total
this_month_completion_rate = lessons_completed/lessons_total
rate_change = this_month_completion_rate - last_month_completion_rate


# =======
# SIDEBAR
# =======


with st.sidebar:
    st.header("⚙️ Controls")
    st.caption("*For Detailed View Only*")

    module_slider = st.slider("Modules to display", 1, 12, value=12)

    module_status = st.selectbox("Status", 
        [
            "Completed",
            "In Progress",
            "Not Started",        
        ],
        index=None,
        placeholder="Select..."
    )


# ====
# MAIN
# ====


st.title("📊 My Software Engineering Dashboard", text_alignment="center")
st.space("medium")


# =======
# METRICS
# =======


m_total, m_not_yet_completed, m_completed, m_completion_rate = st.columns(4)

with m_total:
    st.metric(  # No delta value needed
        "Total Lessons in the Program",
        lessons_total  
    )

with m_not_yet_completed:
    st.metric(
        "Lessons to Complete", 
        lessons_to_complete, 
        delta=(-LESSONS_COMPLETED_BY_MONTH["October"]), 
        delta_color="inverse"
    )
    st.caption("*Compared with last month*")

with m_completed:
    st.metric(
        "Lessons Completed", 
        lessons_completed, 
        delta=LESSONS_COMPLETED_BY_MONTH["October"]
    )
    st.caption("*Compared with last month*")

with m_completion_rate:
    st.metric(
        "Program Completion Rate",
        f"{this_month_completion_rate * 100:.1f}%",
        delta=f"{rate_change * 100:.1f} pp"
    )
    st.caption("*Compared with last month*")

st.space("small")


# ====
# TABS
# ====


tab_overview, tab_details = st.tabs([
    "📈 Overview", 
    "📋 Details"
])


# OVERVIEW

with tab_overview:
    st.subheader("Lesson Completion Trend")

    overview_df = pd.DataFrame(
        list(LESSONS_COMPLETED_BY_MONTH.items()),
        columns=["Month", "Lessons Completed"]
    )

    st.bar_chart(
        overview_df,
        sort=False,
        x="Month",
        y="Lessons Completed",
        x_label="Month",
        y_label="Lessons Completed",
        color=["#35493a"]
    )

    with st.expander("💡 A Note Regarding the Overview Chart"):
        st.write("The program began in June 2026 and is expected to be completed in December 2026.")


# DETAILS

cumulative_lessons = 0
rows = []

for module in MODULES:  # Determine module completion status
    previous_cumulative = cumulative_lessons
    
    cumulative_lessons += module["num_lessons"]

    if lessons_completed >= cumulative_lessons:
        status = "Completed"

    elif lessons_completed < cumulative_lessons and lessons_completed >= previous_cumulative: 
        status = "In Progress"

    else:  # If lessons_completed < BOTH previous_cumulative and cumulative_lessons
        status = "Not Started"

    rows.append({
        "Module": module["number"],
        "Title": module["title"],
        "Number of Lessons": module["num_lessons"],
        "Status": status
    })

details_df = pd.DataFrame(rows)

with tab_details:
    st.subheader("Lesson Completion Details")

    filtered_df = details_df.copy()  
    
    if module_status:  # If a value from the sidebar status selectbox is selected, filter for status
        filtered_df = filtered_df[filtered_df["Status"] == module_status]  

    filtered_df = filtered_df.iloc[:module_slider]  # Show only the number of modules selected in the sidebar       

    st.dataframe(
        filtered_df,
        height="content",     
        hide_index=True
    )

    with st.expander("💡 A Note Regarding the Details Chart"):
        st.write("The counts included here do not reflect 'Knowledge Checks' included in some Modules.")