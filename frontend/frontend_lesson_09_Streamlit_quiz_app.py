import streamlit as st


# ===========
# PAGE CONFIG
# ===========


st.set_page_config(
    page_title = "Test Your Knowledge",
    page_icon = "🤯",
    layout = "wide"
)

st.title("🤯 Test Your Knowledge")


QUESTIONS = [
    {
        "question": "What does HTTP stand for?",
        "options": [
            "Handoff Text To Python",
            "Hyper Text Markup Language",
            "Hyper Text Transfer Protocol",
            "Handle Transfer To Programming"
        ],
        "answer": 2,
        "explanation": "The correct answer is 'Hyper Text Transfer Protocol'. 'Handoff Text To Python' and 'Handle Transfer To Programming' don't exist, and 'Hyper Text Markup Language' refers to HTML."
    },
    {
        "question": "Which status code means 'Not Found'?",
        "options": [
            "201",
            "401",
            "404",
            "422"
        ],
        "answer": 2,
        "explanation": "The correct answer is 404. 201 refers to 'Created', 401 refers to 'Unauthorized', and 422 is a 'Validation Error'."
    },
    {
        "question": "What does CSS stand for?",
        "options": [
            "Controlled Style Sheet",
            "Cascading Style Sheet",
            "Custom Style Sheet",
            "Complicated Style Sheet"
        ],
        "answer": 1,
        "explanation": "The correct answer is 'Cascading Style Sheet'. The remaining options are not real."
    },
    {
        "question": "What does DOM stand for?",
        "options": [
            "Document Object Model",
            "Document ORM Model",
            "Database Object Model",
            "Document Object Markup"
        ],
        "answer": 0,
        "explanation": "The correct answer is 'Document Object Model'. The remaining options are not real."
    },
    {
        "question": "Which Python library do we use for HTTP requests?",
        "options": [
            "fastapi",
            "restapi",
            "uvicorn",
            "requests"
        ],
        "answer": 3,
        "explanation": "The correct answer is 'requests'. 'restapi' is not a library, 'fastapi' is related to requests but not directly used to make HTTP requests, and 'uvicorn' refers to a web-server implementation."
    },
    {
        "question": "Where should the page config go in a Streamlit script?",
        "options": [
            "At the very top",
            "After the imports",
            "At the very bottom",
            "Anywhere is fine"
        ],
        "answer": 1,
        "explanation": "The correct answer is 'After the imports'. This must be the first command in the script, otherwise it will produce an error."
    }
]


# =====================
# STATE INITIALIZATIONS
# =====================


if 'current_question' not in st.session_state:
    st.session_state["current_question"] = 0

if 'score' not in st.session_state:
    st.session_state["score"] = 0

if 'answered' not in st.session_state:
    st.session_state["answered"] = False

if 'selected' not in st.session_state:
    st.session_state["selected"] = None

if 'show_results' not in st.session_state:
    st.session_state["show_results"] = False


# ==============
# RESULTS SCREEN
# ==============


if st.session_state.show_results:
    total = len(QUESTIONS)
    score = st.session_state["score"]

    percentage_score = (score / total) * 100

    if percentage_score == 100:
        st.success(f"Great job! You scored {score} out of {total} ({percentage_score:.2f}%)! Click 'Restart' to try again.")
        st.balloons()

    elif percentage_score >= 75:
        st.warning(f"Good try! You scored {score} out of {total} ({percentage_score:.2f}%). Click 'Restart' to try again.")

    else:
        st.error(f"Uh-oh! You scored {score} out of {total} ({percentage_score:.2f}%). Click 'Restart' to try again.")

    st.progress(percentage_score / 100)

    if st.button(
        "Restart", 
        key="restart"
    ):
        st.session_state.clear()  # Reset all state keys        
        st.rerun()  # Refresh the page

    st.stop()  # Called so quiz does not render


# ===========
# QUIZ SCREEN
# ===========


current_question_index = st.session_state["current_question"]
question_by_index = QUESTIONS[current_question_index]
total_questions = len(QUESTIONS)

st.write(f"Question {current_question_index + 1} out of {total_questions}")
st.progress((current_question_index + 1) / total_questions)

st.subheader(f"{question_by_index['question']}")


# ==================
# QUIZ RADIO BUTTONS
# ==================


selected = st.radio(
    "Select an answer:",
    question_by_index["options"],
    index=None if not st.session_state["answered"] else st.session_state["selected"],  # If the player has not selected an answer, the buttons remain empty; otherwise, the button will reflect the selected answer
    disabled=st.session_state["answered"],  # If the player has submitted an answer, disable the radio buttons
    key=f"q_{current_question_index}"
)

if selected is not None and not st.session_state["answered"]:  # If the player has selected but not submitted their answer, store their selection in state
    st.session_state["selected"] = question_by_index["options"].index(selected)


# ==================
# QUIZ SUBMIT BUTTON
# ==================


if not st.session_state["answered"]:  # If the player has not yet answered, display the Submit button
    if st.button(
        "Submit",
        key=f"submit_{current_question_index}",
        disabled=True if st.session_state["selected"] is None else False  # Disable the Submit button until the player selects an answer
    ):
        st.session_state["answered"] = True  # Mark in state that the player has submitted an answer
        if st.session_state["selected"] == question_by_index["answer"]:  # Increment the score if the answer is correct
            st.session_state.score += 1
        st.rerun()  # Refresh the page to continue on


# =============
# QUIZ FEEDBACK
# =============


if st.session_state["answered"]:  # If the player has submitted an answer

    if st.session_state["selected"] == question_by_index["answer"]:  # If the answer is correct
        st.success("Correct!")

    else:  # If the answer is incorrect
        st.error("That is incorrect.")
        st.info(f"{question_by_index['explanation']}")

    if current_question_index == total_questions - 1:  # If that was the last question
        if st.button(
            "Finish",
            key="finish"
        ):
            st.session_state["show_results"] = True
            st.rerun()
        
    else:  # If that was not the last question
        if st.button(
            "Next",
            key=f"next_from_{current_question_index}"
        ):
            st.session_state["current_question"] += 1
            st.session_state["answered"] = False
            st.session_state["selected"] = None
            st.rerun()