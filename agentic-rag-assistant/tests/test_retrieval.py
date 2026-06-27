from vectorstore.pinecone_client import query_vectors

from services.llm import generate_answer


# ---------------- RUN TEST ----------------

question = "Who is CEO and director of Panaversity?"

# STEP 1: retrieve chunks
chunks = query_vectors(question)

# STEP 2: generate answer
answer = generate_answer(question, chunks)

# ---------------- OUTPUT ----------------

print("\n===== QUESTION =====\n")
print(question)

print("\n===== RETRIEVED CHUNKS =====\n")

for i, c in enumerate(chunks[:3]):
    print(f"\nChunk {i+1} (score: {c.get('score', 0)})")
    print(c["metadata"]["text"][:300])

print("\n===== FINAL ANSWER =====\n")
print(answer)

