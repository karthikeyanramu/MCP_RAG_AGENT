"""
RAG TOOL IMPLEMENTATION

This file converts your RAG pipeline into a reusable TOOL.

Tool Name: knowledge_search

What it does:
- Takes a query
- Searches vector DB
- Returns relevant context

IMPORTANT:
- This will be called by the Agent later
- Keep it simple and reusable
"""

# Load required libraries
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔹 STEP 1: Load knowledge base (your file)
loader = TextLoader("data/knowledge.txt")
documents = loader.load()

# 🔹 STEP 2: Convert to embeddings (LOCAL - no API)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 🔹 STEP 3: Create vector database
db = Chroma.from_documents(documents, embeddings)

# 🔹 STEP 4: Define TOOL function
def knowledge_search(query: str) -> str:
    """
    TOOL: knowledge_search

    Input:
        query (str) → user question

    Output:
        str → relevant context from knowledge base
    """

    # Search similar documents
    results = db.similarity_search(query)

    # Take top 2 results for better context
    context = "\n".join([doc.page_content for doc in results[:2]])

    return context


# 🔹 (Optional) Local test
if __name__ == "__main__":
    test_query = "What is RAG?"
    print("Test Query:", test_query)
    print("\nTool Output:\n", knowledge_search(test_query))