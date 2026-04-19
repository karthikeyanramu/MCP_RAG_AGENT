"""
RAG (Retrieval Augmented Generation) - Fully Local Implementation

This script demonstrates a simple end-to-end RAG pipeline using only local components.

What this program does:
1. Loads a text file (knowledge base) containing domain-specific information.
2. Converts the text into vector embeddings using a local embedding model 
   (HuggingFace - all-MiniLM-L6-v2).
3. Stores these embeddings in a local vector database (Chroma).
4. Accepts a user query as input.
5. Searches the vector database to retrieve the most relevant content.
6. Sends the retrieved context along with the query to a local LLM 
   (running via Ollama - llama3 model).
7. Generates a final answer based strictly on the retrieved context.

Key Advantages:
- Fully local execution (no external API calls)
- No cost involved
- Faster for small datasets
- Suitable for learning RAG concepts and prototyping

Flow:
User Query → Embeddings → Vector Search (Chroma) → Context Retrieval → LLM (Ollama) → Answer
"""

import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

# LOCAL embeddings (no API)
from langchain_community.embeddings import HuggingFaceEmbeddings

# LOCAL LLM via Ollama
from langchain_community.chat_models import ChatOllama

# STEP 1: Load file
loader = TextLoader("data/knowledge.txt")
documents = loader.load()

# STEP 2: Local embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# STEP 3: Store in vector DB
db = Chroma.from_documents(documents, embeddings)

# STEP 4: User query
query = input("Ask your question: ")

# STEP 5: Retrieve context
results = db.similarity_search(query)

context = "\n".join([doc.page_content for doc in results[:2]])

print("\n🔍 Retrieved Context:")
print(context)

# STEP 6: Local LLM (Ollama)
llm = ChatOllama(model="llama3")

prompt = f"""
Answer the question based only on the context below:

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

print("\n🤖 Final Answer:")
print(response.content)