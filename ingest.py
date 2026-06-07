import os
import chromadb
from chromadb.utils import embedding_functions

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r") as f:
                text = f.read()
            docs.append({"filename": filename, "text": text})
    return docs

def chunk_document(doc, chunk_size=400, overlap=50):
    text = doc["text"]
    filename = doc["filename"]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append({"text": chunk, "source": filename})
        start += chunk_size - overlap
    return chunks

def build_vector_store():
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))

    print(f"Total chunks: {len(all_chunks)}")

    client = chromadb.PersistentClient(path="./chroma_db")
    ef = embedding_functions.DefaultEmbeddingFunction()

    try:
        client.delete_collection("professor_reviews")
    except:
        pass

    collection = client.create_collection(
        "professor_reviews",
        embedding_function=ef
    )

    texts = [c["text"] for c in all_chunks]
    sources = [c["source"] for c in all_chunks]
    ids = [f"chunk_{i}" for i in range(len(texts))]

    collection.add(
        documents=texts,
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )

    print("Vector store built successfully!")

if __name__ == "__main__":
    build_vector_store()