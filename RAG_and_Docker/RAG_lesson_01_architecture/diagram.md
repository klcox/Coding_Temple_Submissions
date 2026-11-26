# End-to-End RAG Pipeline

| Step | Technology | What Happens | Data |
|---|---|---|---|
| 1 | User Interface (e.g. Streamlit) | User enters a question/query | Query (string) |
| 2 | SentenceTransformer | The user's question is converted to an embedding vector using the same model which embedded the documents. | Query Embedding | 
| 3 | ChromaDB | The embedded query is compared against the embedded documents stored in the vector database to assess similarity. Then, the most similar chunks are retrieved. | Relevant Chunk Results | 
| 4 | Python | The chunk results (context) are combined with a system prompt and the user's original query into a single prompt for the LLM. | Prompt | 
| 5 | Ollama | The LLM receives the complete prompt and generates a response based only on the prompt/context provided. The response then is returned to the user. | LLM Response |