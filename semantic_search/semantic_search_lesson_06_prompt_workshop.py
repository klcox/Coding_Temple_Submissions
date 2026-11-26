def mock_response(prompt):
    """Simulates varied AI reponses based on prompt quality."""

    prompt_lower = prompt.lower()

    # Detect if the prompt has framing
    has_role = any(word in prompt_lower for word in ["you are", "act as", "your role"])

    # Detect if the prompt has constraints
    has_constraints = any(word in prompt_lower for word in
        ["under 100", "200-word", "words or fewer", "in 3 sentences", "as a table", "as json", "format", "bullet"])
    
    # Detect if the prompt has examples
    has_examples = "input:" in prompt_lower or "example" in prompt_lower


    quality_score = sum([has_role, has_constraints, has_examples])

    if quality_score >= 3:
        responses = {
            "code_explanation": "\n  [MOCK RESPONSE — Good] In Streamlit, st.session_state is a built-in feature that stores variables and preserves their values across app reruns, allowing you to maintain information such as user inputs, login status, shopping cart items, or selected filters. You should use it whenever your application needs to remember information between user interactions, such as tracking button clicks, maintaining form data, or managing application state, and you can initialize and update values using syntax like st.session_state['count'] = 0 and st.session_state['count'] += 1. For example, in a sample frontend project like a shopping cart, you could use st.session_state to store selected products, update the cart when users click an 'Add to Cart' button, and dynamically display the cart's contents and total price without losing previously selected items whenever Streamlit reruns the application.",
            "data_formatting": """\n  [MOCK RESPONSE — Good] [
                {
                    "title": "Do Homework",
                    "priority": "high",
                    "status": "pending"
                },
                {
                    "title": "Clean Kitchen",
                    "priority": "low",
                    "status": "pending"
                },
                {
                    "title": "Finish Laundry",
                    "priority": "medium",
                    "status": "done"
                }
            ]""",
            "system_prompt": """\n  [MOCK RESPONSE — Good] HTML defines content for a webpage using tags to mark up and organize content. Tags identify elements such as headings, paragraphs, navigation menus, and images, defining the webpage's structure and what content is present. Source document: html_intro.txt
            """
        }
    
    else:       
        responses = {
            "code_explanation": "\n  [MOCK RESPONSE — Bad] Streamlit's st.session_state stores variables outside of the main script to aid persistence.",
            "data_formatting": """\n  [MOCK RESPONSE — Bad] Sure! You can create a simple bulleted list. I would recommend the following order: 
                * Do Homework (medium)
                * Finish Laundry (medium)
                * Clean Kitchen (low)
            """,
            "system_prompt": "\n  [MOCK RESPONSE — Bad] Absolutely! How can I help?"
        }

    return responses


print("Task 1: Code Explanation")

bad_prompt_code = "    Tell me about Streamlit's st.session_state."
print(f"\n  Bad Prompt:")
print(bad_prompt_code)
bad_response_code = mock_response(bad_prompt_code)
print(bad_response_code["code_explanation"])

good_prompt_code = "    Act as an instructor of a coding bootcamp and explain what st.session_state does in Streamlit. For example, include how it is used, when it should be used, and how to incorporate it into a sample frontend project. Response format should be 3-sentences."
print(f"\n  Good Prompt:")
print(good_prompt_code)
good_response_code = mock_response(good_prompt_code)
print(  good_response_code["code_explanation"])


print("\n\nTask 2: Data Formatting")

bad_prompt_data = "    Take this list of tasks and organize them into something useful. Give each task the right priority and status, and ensure that it is easy to read. Tasks: Do Homework, Clean Kitchen, Finish Laundry."
print(f"\n  Bad Prompt:")
print(bad_prompt_data)
bad_response_data = mock_response(bad_prompt_data)
print(bad_response_data["data_formatting"])

good_prompt_data = "    You are a coding tutor assisting me with a project. Convert this list of tasks into a JSON array format, including title, priority, and status fields. For example, input: 'Do Homework', to-do ; output: {{'title': 'Do Homework', 'priority': 'high', 'status': 'pending}}. Output should refer to one array encompassing all provided tasks. Tasks: Do Homework, urgent, to-do; Clean Kitchen, low, not done; Finish Laundry, medium, done."
print(f"\n  Good Prompt:")
print(good_prompt_data)
good_response_data = mock_response(good_prompt_data)
print(good_response_data["data_formatting"])


print("\n\nTask 3: System Prompt Design")

bad_prompt_system = "    I need you to help me with my programming course."
print(f"\n  Bad Prompt:")
print(bad_prompt_system)
bad_response_system = mock_response(bad_prompt_system)
print(bad_response_system["system_prompt"])

system_prompt = """\n\n    System Prompt: Your role is a Course Study Assistant that answers questions based only on provided context from my course notes. If the context does not contain the answer, be honest and say so. For example, in that scenario, just explain that an answer is not available based on the current context. Please keep responses 150 words or fewer, and include the source document from where you derived the answer.
"""
good_prompt_system = """    <html_intro.txt> 
HTML is the frame of every webpage. It defines the structure: 'This is a heading. This is a paragraph. This is a navigation menu. This is an image.' It doesn't say anything about colors, fonts, or what happens when you click something - that's CSS and JavaScript, which you'll learn in the next two lessons. HTML just says what's there and how it's organized. HTML uses tags to mark up content. A tag is a keyword wrapped in angle brackets: <p>This is a paragraph.</p>

How does HTML define content for a webpage?"""
print(f"\n  Good Prompt:")
print(good_prompt_system)
good_response_system = mock_response(system_prompt)
print(  good_response_system["system_prompt"])