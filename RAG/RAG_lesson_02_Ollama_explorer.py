import requests
import time


OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"


def generate(prompt, system = None):
    """Send a prompt to Ollama and return the response."""

    start = time.time()

    response = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "stream": False  # Wait for the complete response
    })

    elapsed = time.time() - start
    data = response.json()
    text = data["message"]["content"]

    print(f"  [Generated in {elapsed:.1f}s]")
    return text


# ===========
# EXPERIMENTS
# ===========


print("Experiment 1: Same Question, Different System Prompts")

prompt = "What is an API?"

print("\n  Test 1 - No System Prompt\n")
response_1 = generate(prompt=prompt)
print(f"    {response_1}")

print("\n  Test 2 - Explain Like I'm 5 Years Old\n")
response_2 = generate(prompt=prompt, system="Explain like I'm 5 years old.")
print(f"    {response_2}")

print("\n  Test 3 - Senior Software Architect\n")
response_3 = generate(prompt=prompt, system="You are a senior software architect. Be technical and precise.")
print(f"    {response_3}")

print("\n**EXPERIMENT COMMENTARY**:")
print("Responses 1 and 3 are largely similar in topics covered and length. In some cases, even the exact wording is the same across both responses! However, response 1 (no system prompt) uses language that is a bit more accessible to a general inquirer, whereas response 3 (senior software architect) contains slightly more technical language that likely would be more familiar to an inquirer with that job title. Response 2 (explain like I'm 5 years old) attempted to use simpler language and more analogies so that a younger person could understand, but, ultimately, I still found the response not quite suitable for a 5-year-old as it remained too complex and technical. Thus, it could use more refinement were it to be shared with that age group.")


print("\n\nExperiment 2: RAG-Style Context Grounding")

context = "Both Korean and Japanese languages use multiple hierarchies of speech, such as informal (reserved for extremely close peers, siblings, children, and those of lower standing) and formal (used when addressing or referring to the elderly, senior staff, etc.). The languages also use different counter words for different objects, such as different counters for paper objects, food, animals, people, etc. The languages even have some words that sound incredibly similar due to shared histories."

system = f"Answer the user's question based ONLY on the following context. Do not take information from any other source in order to generate the response. If the context doesn't contain the answer, say 'I don't have enough information to answer at this time.'\n\nCONTEXT: {context}"

print("\n  Test A - CAN Be Answered from Context\n")
response_A = generate(prompt="When is formal speech used in Korean?", system=system)
print(f"    {response_A}")

print("\n  Test B - CANNOT Be Answered from Context\n")
response_B = generate(prompt="How are French and Spanish similar?", system=system)
print(f"    {response_B}")

print("\n**EXPERIMENT COMMENTARY**:")
print("Interestingly enough, when I first ran the queries, the model added a little external context when responding to the first prompt and completely ignored my instructions for the second prompt as it produced a complete response from its general knowledge instead of responding with 'I don't have enough information to answer at this time.' As a result, I went back and added to the system prompt: 'Do not take information from any other source in order to generate the response.' Upon running the queries again, it added multiple paragraphs of information outside of the context when responding to the first query; when responding to the second query, this time it did include my designated response, yet it still added an additional question prompting the user for more information. This demonstrates the significant importance of a strong system prompt and safeguards as models can be unpredictable.")


print("\n\nExperiment 3: Response Timing")

print("\n  Test 1 - Short Question Length\n")
response_short = generate(prompt="What is HTML used for?")
print(f"    {response_short}")

print("\n  Test 2 - Medium Question Length\n")
response_medium = generate(prompt="Can you please explain how HTML, CSS, and Bootstrap all work together for frontend development of simple webpages and apps?")
print(f"    {response_medium}")

print("\n  Test 3 - Long Question Length\n")
response_long = generate(prompt="Why is learning Spanish important in today’s globalized society, and how can understanding its grammar, vocabulary, and cultural expressions help individuals communicate effectively with native speakers, appreciate the traditions and lifestyles of Spanish-speaking communities, build meaningful relationships, foster empathy, and create new opportunities in education, travel, business, and everyday life?")
print(f"    {response_long}")

print("\n**EXPERIMENT COMMENTARY**:")
print("When I ran the queries, the short question produced a response in the shortest time (~20 seconds), and the medium question took a longer time to produce a response (~40 seconds), both as expected. However, I was surprised to see that the long question fell right in the middle at ~30 seconds as I would have expected that it would take the longest of the 3 queries. This left me to wonder if the topic may have influenced the results as queries 1 and 2 are relatively similar in referencing web development, whereas query 3 pertains to foreign languages.")