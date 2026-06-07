import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_collection("professor_reviews", embedding_function=ef)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    results = collection.query(query_texts=[question], n_results=5)

    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    context = "\n\n".join([f"[Source: {s}]\n{c}" for s, c in zip(sources, chunks)])

    prompt = f"""You are a helpful assistant that answers questions about CST professors 
at New York City College of Technology based ONLY on the student reviews provided below.

If the provided reviews do not contain enough information to answer the question, 
say exactly: "I don't have enough information on that."

Do NOT use any outside knowledge. Only answer from the reviews below.

Student Reviews:
{context}

Question: {question}

Answer (cite which professor/source your answer comes from):"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    answer = response.choices[0].message.content
    unique_sources = list(set(sources))
    return {"answer": answer, "sources": unique_sources}

if __name__ == "__main__":
    result = ask("Is Professor Chen's class easy?")
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])