# main.py
import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
from google import genai
from google.genai import types
import re

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "AIzaSyDTrJGYOwBdZvkO2OHKX65Zm1FRLaWhuRU "
DATA_FILES = ["sample.txt", "sample1.txt", "sample2.txt", "sample3.txt", "sample4.txt", "sample5.txt"]
EMBEDDING_MODEL = "models/gemini-embedding-001"  # Must match your stored embeddings
MODEL_ID = "gemini-3-flash-preview"  # for generating answers

os.environ["GENAI_API_KEY"] = API_KEY
# main.py

# List all your data files
DATA_FILES = ["sample.txt", "sample1.txt", "sample2.txt", "sample3.txt", "sample4.txt", "sample5.txt"]

def query_rag(question: str):
    if not question.strip():
        return "No question provided."

    # Step 1: Make sure ChromaDB has all documents embedded
    if collection.count() == 0:
        total_chunks = 0
        for file_name in DATA_FILES:
            if not os.path.exists(file_name):
                print(f"File not found: {file_name}")
                continue

            with open(file_name, "r", encoding="utf-8") as f:
                text = f.read()

            # Split text into manageable chunks
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)

            # Add chunks to ChromaDB collection
            collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=[{"source": file_name} for _ in chunks],
                ids=[f"{file_name}_id_{i}" for i in range(len(chunks))]
            )
            total_chunks += len(chunks)
            print(f"Stored {len(chunks)} chunks from '{file_name}'")

        print(f"Total chunks stored in ChromaDB: {total_chunks}")

    # Step 2: Embed the user query
    query_result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[question],
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    query_embedding = query_result.embeddings[0].values

    # Step 3: Search ChromaDB for relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3  # top 3 relevant chunks
    )

    top_passages = results["documents"][0]
    if not top_passages:
        return "No relevant passages found in the knowledge base."

    # Step 4: Combine passages into context
    context = "\n".join(top_passages)

    # Step 5: Build the prompt
    prompt = f"""
    Use the context below to answer the question.
    Context:
    {context}

    Question:
    {question}
    """

    # Step 6: Generate answer using Gemini
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )

    return response.candidates[0].content
# -----------------------------
# Initialize Clients
# -----------------------------
client = genai.Client(api_key=API_KEY)
chroma_client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)
collection = chroma_client.get_or_create_collection(name="my_collection")

# -----------------------------
# Helpers
# -----------------------------
def chunk_text(text, chunk_size=200):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def embed_chunks(chunks):
    """Embed text chunks using Gemini and return float vectors."""
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=chunks,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    return [item.values for item in result.embeddings]

def generate_prompt(query, passage):
    """Construct a user-friendly prompt from query and reference passage."""
    escaped = passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = f"""
    You are a helpful and informative bot that answers questions using
    text from the reference passage included below.
    Be sure to respond in a complete sentence, being comprehensive,
    including all relevant background information.
    Talk to a non-technical audience in a friendly, conversational tone.
    If the passage is irrelevant, you may ignore it.

    QUESTION: '{query}'
    PASSAGE: '{escaped}'

    ANSWER:
    """
    return prompt

def generate_answer(query, passage):
    """Generate answer from Gemini using a single passage."""
    prompt = generate_prompt(query, passage)
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    # Extract text from response
    return response.candidates[0].content

# -----------------------------
# Main
# -----------------------------
def main():
    # Read & embed data only if DB is empty
    if collection.count() == 0:
        total_chunks = 0
        for file_name in DATA_FILES:
            if not os.path.exists(file_name):
                print(f"File not found: {file_name}")
                continue

            with open(file_name, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)

            collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=[{"source": file_name} for _ in chunks],
                ids=[f"{file_name}_id_{i}" for i in range(len(chunks))]
            )
            total_chunks += len(chunks)
            print(f"Stored {len(chunks)} chunks from '{file_name}'")

        print(f"Total chunks stored in ChromaDB: {total_chunks}")

    # Interactive loop
    while True:
        query = input("\nEnter your question (or 'exit' to quit): ")
        if query.lower() == "exit":
            break

        # Embed query
        query_result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=[query],
            config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
        )
        query_embedding = query_result.embeddings[0].values

        # Search ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        top_passages = results['documents'][0]
        if not top_passages:
            print("No relevant passages found.")
            continue

        # Generate answer
        answer = generate_answer(query, top_passages[0])
        print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()