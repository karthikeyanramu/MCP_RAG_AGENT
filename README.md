# MCP RAG Agent – End-to-End Beginner Guide

This repository demonstrates a **Modular AI Testing & API Agent System** combining:

* 🔎 RAG (Retrieval Augmented Generation)
* 🧠 MCP (Model Control/Tool Execution Layer)
* 🌐 API Testing Agent (Postman-like automation layer)

It is designed to help QA Engineers and Developers build **intelligent API testing systems powered by AI + tools + knowledge retrieval**.

---

# 📌 1. Project Overview (Simple Explanation)

Think of this system like 3 layers working together:

## 🧩 Layer 1: RAG (Knowledge Brain)

* Stores documents / knowledge
* Retrieves relevant context for a query
* Helps AI answer with domain knowledge

👉 Example:

> “What is a SWIFT payment?” → RAG fetches banking knowledge

---

## 🧩 Layer 2: MCP Server (Tool Executor)

* Acts as a **tool manager / middleware**
* Exposes tools like:

  * `knowledge_search`
  * `calculator`
  * API execution tools

👉 Example:

> AI says: “Call API with payload X” → MCP executes it

---

## 🧩 Layer 3: API Agent (Test Engine)

* Reads user input (natural language)
* Converts into API test steps
* Executes API calls
* Validates response

👉 Example:

> “Test login API with valid credentials” → system runs API call + validation

---

# 🔁 End-to-End Flow (Very Important)

```
User Query
   ↓
API Agent (understands intent)
   ↓
MCP Server (chooses tools)
   ↓
RAG (fetches knowledge if needed)
   ↓
API Execution Layer (requests sent)
   ↓
Response Validation
   ↓
Final Output to User
```

---

# 🧰 2. Project Structure (Expected)

```
MCP_RAG_AGENT/
│
├── qa_agent/
│   ├── api_agent_runner.py
│   ├── mcp_client.py
│
├── tools/
│   ├── rag_tool.py
│   ├── calculator_tool.py
│
├── server/
│   ├── mcp_server.py
│
├── data/
│   ├── documents/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ 3. Installation Steps

## ✅ Step 1: Clone Repository

```bash
git clone https://github.com/karthikeyanramu/MCP_RAG_AGENT.git
cd MCP_RAG_AGENT
```

---

## ✅ Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows:

```bash
venv\Scripts\activate
```

### Mac/Linux:

```bash
source venv/bin/activate
```

---

## ✅ Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements missing:

```bash
pip install flask requests numpy pandas
```

---

# 🚀 4. Running the System (Step-by-Step)

## 🔹 Step 1: Start MCP Server

```bash
python server/mcp_server.py
```

Expected output:

```
MCP Server running on http://localhost:5000
Tools loaded: knowledge_search, calculator
```

---

## 🔹 Step 2: Run API Agent

Open a NEW terminal:

```bash
python -m qa_agent.api_agent_runner
```

---

## 🔹 Step 3: Send Query

Inside runner:

```text
Test login API with valid credentials
```

OR

```text
What is SWIFT payment and validate API response format
```

---

# 🧠 5. How Each Layer Works Internally

---

## 🔎 RAG Layer (rag_tool.py)

### Responsibilities:

* Load documents
* Convert to embeddings (if implemented)
* Retrieve relevant chunks

### Flow:

```
User Query → Search Documents → Return Context
```

---

## ⚙️ MCP Server Layer

### Responsibilities:

* Expose tools via API
* Accept execution requests
* Route to correct tool

### Example endpoints:

```
POST /execute
GET /tools
```

---

## 🧪 API Agent Layer

### Responsibilities:

* Parse natural language
* Build API request
* Call MCP tools
* Validate response

### Example:

```python
request = {
  "method": "POST",
  "url": "/login",
  "body": {...}
}
```

---

# 🔄 6. Example Execution Flow

## Input:

```
Test user login API with valid credentials
```

## System Processing:

1. API Agent detects intent → "Login API test"
2. MCP decides tool → API execution tool
3. RAG provides context → login payload structure
4. API call executed
5. Response validated

---

## Output:

```
STATUS: 200 OK
LOGIN SUCCESS
Response validated successfully
```

---

# 🧪 7. Available Tools

## 🔹 knowledge_search

* Searches documents

## 🔹 calculator

* Performs calculations

## 🔹 API Executor (custom)

* Sends HTTP requests

---

# 🛠️ 8. Common Commands

## Run server

```bash
python server/mcp_server.py
```

## Run agent

```bash
python -m qa_agent.api_agent_runner
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚠️ 9. Common Issues

## ❌ Port already in use

```bash
netstat -ano | findstr :5000
```

Kill process:

```bash
taskkill /PID <pid> /F
```

---

## ❌ Module not found

```bash
pip install -r requirements.txt
```

---

# 🎯 10. Real-World Use Cases

* API Test Automation using AI
* Banking domain API validation
* AML / KYC system testing
* Smart QA Agent for regression testing

---

# 🚀 11. Future Enhancements

* OpenAI / LLM integration
* Postman collection import
* UI dashboard
* CI/CD pipeline integration
* Advanced RAG embeddings

---

# 👨‍💻 12. Summary

This project demonstrates:

✔ AI-powered API testing
✔ Modular tool execution (MCP)
✔ Knowledge-driven responses (RAG)
✔ Real-world QA automation framework
