from sentence_transformers import SentenceTransformer, util


knowledge_base = [
    # Python/API Development
    "FastAPI automatically generates interactive API documentation using Swagger UI.",
    "JWT tokens are used for stateless authentication in REST APIs.",
    "SQLAlchemy is an ORM that maps Python classes to database tables.",
    "You can combine Streamlit, FastAPI, and SQLAlchemy to design a complete app with a frontend interface and backend routing/storage.",
    "API stands for Application Programming Interface.",
    # Language Study
    "Japanese utilizes three different writing systems: hiragana, katakana, and kanji.",
    "Both Korean and Japanese languages utilize honorific forms of speech in certain contexts as well as counter words for different objects.",
    "The Korean alphabet was derived by King Sejong the Great during the Joseon dynasty (~1445).",
    "Spanish, French, and Italian are considered romance languages.",
    "Spanish, French, and Italian have similar vocabulary and grammar structures as they share Latin roots.",
    # Founding of America
    "Founding fathers of America include George Washington, Thomas Jefferson, Benjamin Franklin, James Madison, and Alexander Hamilton.",
    "George Washington was the first president of the United States.",
    "Thomas Jefferson is the principle author of the Declaration of Independence.",
    "James Madison is the primary author of the Constitution.",
    "The Declaration of Independence was signed on August 2, 1776."
]

queries = [
    "What similarities exist between languages?",
    "What do I need for an app that uses an API?",
    "Who was involved in the founding of America?",
    "What tool should I use when creating a database?",
    "Who wrote the Constitution?"
]

THRESHOLDS = [0.3, 0.5, 0.7]


model = SentenceTransformer("all-MiniLM-L6-v2")
sentence_embeddings = model.encode(knowledge_base)  # Embed the knowledge base sentences


for query in queries:
    print(f'\nQuery: "{query}"')

    query_embedding = model.encode(query)  # Embed the query
    similarity_scores = util.cos_sim(query_embedding, sentence_embeddings)[0]  # Calculate similarity scores, comparing the query against all sentences in the knowledge base
    similarity_scores = list(enumerate(similarity_scores))  # Include the index with each score so as to denote the associated sentence

    for threshold in THRESHOLDS:
        filtered_sentences = [s for s in similarity_scores if s[1] >= threshold]  # Filter to include only sentences that meet or exceed the current score threshold
        missed_sentences = [s for s in similarity_scores if s[1] < threshold and s[1] >= 0.3]  # Filter to include only sentences that are below the current score threshold yet which are at or above 0.3

        # Sort filtered sentence lists
        filtered_sentences.sort(key=lambda x: x[1].item(), reverse=True)
        missed_sentences.sort(key=lambda x: x[1].item(), reverse=True)   
                
        # Print results        
        print(f"\n  Threshold {threshold}: {len(filtered_sentences)} result(s)")
        for index, score in filtered_sentences:
            print(f"    [{score.item():.3f}] {knowledge_base[index]}")

        if missed_sentences:
            print("\n  Missed Sentences with Potentially Relevant Content")
            for index, score in missed_sentences:
                print(f"    [{score.item():.3f}] {knowledge_base[index]}")

print("\nThis experiment demonstrates that thresholds which are too strict may exclude potentially relevant search results.")