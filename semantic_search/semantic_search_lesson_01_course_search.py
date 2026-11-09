from sentence_transformers import SentenceTransformer, util


sentences = [
    "FastAPI automatically generates interactive API documentation using Swagger UI.",
    "Use pip install to add Python packages to your virtual environment.",
    "SQLAlchemy is an ORM that maps Python classes to database tables.",
    "Streamlit re-runs the entire script every time a user interacts with a widget.",
    "JWT tokens are used for stateless authentication in REST APIs.",
    "The requests library lets you make HTTP calls from Python.",
    "CSS Flexbox arranges elements in a row or column with flexible sizing.",
    "ChromaDB stores document embeddings for fast similarity search.",
    "Embeddings capture relationships between concepts rather than what individual words mean.",
    "Keyword search matches exact words; semantic search matches meaning.",
    "Embeddings convert text into a list of numbers (a vector) that represents the meaning of that text."
]

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence_embeddings = model.encode(sentences)  # Use the model to convert the sentences into an embedding (vector)


def query_CLI():
    """    
    Runs the semantic search CLI.

    1. Converts the query to an embedding (vector); then uses the model to compare the query vector with the sentences vectors using cosine similarity and receives the resulting similarity scores for each comparison. The result is something like [0.82, 0.95, 0.25] according to the number of sentences.

    2. Enumerates the similarity scores so that they now look something like the following in order to include their associated index [
        (0, 0.82),
        (1, 0.95),
        (2, 0.25)
    ].

    3. Sorts the above in reverse (descending) order based on score.

    4. Enumerates the top 3 rankings (beginning at 1) so that they now look something like [
        (1, (1, 0.95)),
        (2, (0, 0.82)),
        (3, (2, 0.25))
    ]

    5. Prints the top 3 results and continues the loop until the user enters 'quit'.    
    """

    print("\nSearch for similar sentences based on meaning. Enter 'quit' to exit the program.")
    
    while True:        
        
        query = input("\nSearch: ").strip()

        if query.lower() == "quit":
            print("Exiting program.")
            break

        elif not query:
            print("That is not a valid entry. Please enter a query or 'quit'.")
            continue

        else:
            embedded_query = model.encode(query)

            similarity_scores = util.cos_sim(embedded_query, sentence_embeddings)[0]

            ranked = sorted(enumerate(similarity_scores), key=lambda x: x[1], reverse=True)

            print(f"Query: '{query}'\n")
            print("Top 3 Results:\n")
            print(f"{'Rank'} | {'Similarity Score'} | {'Sentence'}")
            print(f"{'-' * 125}")
            for rank, (index, score) in enumerate(ranked[:3], 1):
                print(f"{rank:<4} | {score.item():<16.3f} | {sentences[index]}")
                print(f"{'-' * 125}")


# Run
if __name__ == "__main__":

    query_CLI()