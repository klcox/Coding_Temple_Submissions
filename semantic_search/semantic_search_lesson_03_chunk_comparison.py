from sentence_transformers import SentenceTransformer, util


DOCUMENT = """You've probably heard the term “artificial intelligence” a thousand times. It shows up in news headlines, product marketing, movie plots, and job postings. The problem is that almost none of these sources agree on what it actually means. A toothbrush company says their product uses AI. A movie shows a robot with feelings. A news article warns that AI will replace all jobs by next year. A job posting asks for “AI experience.” None of these are talking about the same thing.

So let's start from scratch. What is AI, really?

Artificial intelligence is software that performs tasks that typically require human judgment, like recognizing images, understanding language, making predictions, or generating new content. Most modern AI does this by learning patterns from data instead of following rules a person wrote by hand.

That's it. Not conscious robots. Not magic. Not a single program that can do everything.

A note on the boundary: older AI systems did follow hand-written rules, and computer scientists still classify those as AI. But when someone says "AI" today, they almost always mean the learning-from-data kind, and that is the kind this course is about. Throughout this course, "AI" means systems that learn patterns from data.

Here's a simple way to think about the difference. Imagine you're building a spam filter for email. The traditional programming approach would be to write rules by hand: “If the email contains the word 'lottery,' mark it as spam. If it comes from an unknown sender, mark it as spam.” You'd write hundreds of these rules, and spammers would find ways around every one of them.

The AI approach is fundamentally different. Instead of writing rules, you give the system thousands of examples of spam and not-spam emails, and it learns the patterns on its own. It figures out which combinations of words, sender patterns, and formatting tend to indicate spam - including patterns you never would have thought to write rules for. That's what “learning from data” means in practice.

Two words you'll see constantly

A model is the finished product of that learning process. It's the file that holds everything the system figured out from the examples, and it's what actually does the work when you use the product. When people talk about "GPT-4" or "the spam model," they mean a model.

Training is the process that produces a model. You show the system a large number of examples, it adjusts itself to get better at the task, and when you stop, what you're left with is the model. Training happens once, up front, and can take weeks. Using the model afterward takes a fraction of a second.

Keep these separate in your head. Training is how the model was made. Everything you do with an AI product is happening after training is finished.

Three ways a machine can be taught

•	Supervised learning - you give the system labeled examples, meaning the correct answer comes attached. The spam filter above is supervised: every training email came marked "spam" or "not spam." This is the most common kind you'll meet.
•	Unsupervised learning - you give the system unlabeled data and ask it to find structure on its own, like grouping customers into segments nobody defined in advance.
•	Reinforcement learning - the system learns by trying things and receiving reward or penalty, the way you'd train a dog or teach a program to play a game.

You don't need to build any of these yet. You do need to recognize the words, because they're how the industry describes what a system is doing.   
"""


# ===================
# CHUNKING STRATEGIES
# ===================


def fixed_chunks(text, size=300, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end].strip())
        start += size - overlap
    
    return [c for c in chunks if c]  # Exclude empty chunks


def paragraph_chunks(text):
    paragraphs = text.strip().split('\n\n')  # Split on double newlines

    return [p.strip() for p in paragraphs if p.strip()]  # Exclude empty paragraphs


# =========
# EMBEDDING
# =========


model = SentenceTransformer("all-MiniLM-L6-v2")

strategies = {  # Un-embedded chunks
    "fixed": fixed_chunks(DOCUMENT),
    "paragraph": paragraph_chunks(DOCUMENT)
}

embedded_chunks = {}

print("Chunks Yielded per Strategy:")

# Display chunk counts and sizes
for strategy, chunks in strategies.items():
    sizes = [len(c) for c in chunks]
    avg = sum(sizes) / len(sizes) if sizes else 0
    print(f"  {strategy.capitalize()}: {len(chunks)} chunks, avg {avg:.0f} chars")

    embedded_chunks[strategy] = model.encode(chunks)


# =======
# QUERIES
# =======


print("\nQuery Testing & Strategy Analysis:")
print("(*Note: Paragraph separations are indicated by '//', and chunks have been truncated to 100 characters for display.)")

queries = [
    "What is AI?",
    "What is the difference between model and training?",
    "How does AI learn?"
]

for query in queries:
    query_embedding = model.encode(query)  # Embed the query

    print(f"\nQuery: '{query}'")

    for strategy, chunks in embedded_chunks.items():
        similarity_scores = util.cos_sim(query_embedding, chunks)[0]  # Get similarity scores, comparing the current query with the current strategy's embedded chunks

        ranked = sorted(enumerate(similarity_scores), key=lambda x: x[1], reverse=True)  # Enumerate to include the chunk index and sort in descending order by score
        
        print(f"\n  Top 2 Results ({strategy.capitalize()}):\n")
        print(f"  {'Rank'} | {'Similarity Score'} | {'Chunk'}")
        print(f"  {'-' * 129}")
        for rank, (index, score) in enumerate(ranked[:2], 1):  # Include rank and display
            print(f"  {rank:<4} | {score.item():<16.3f} | {strategies[strategy][index].replace('\n', '/')[:100] + '...'}")
            print(f"  {'-' * 129}")


# ========
# ANALYSIS
# ========


print("""\nAnalysis:
Fixed-sized chunking produced predictable chunk sizes. However, the results lack context as they are often cut mid-sentence or mid-thought. It also appears that this is the cause for lower similarity scores as compared across queries with paragraph chunking. Hence, fixed chunking is best-suited for unstructured text. 

In contrast, paragraph chunking produces greater context as each paragraph chunk contains a complete thought or topic. For this reason, it is best-suited for structured documents such as the one included here. This is indicated by clearer chunks and higher similarity scores overall. However, it is important to consider that, conceptually, paragraph size can vary widely, thus producing different chunk sizes, which may ultimately impact similarity score.
""")