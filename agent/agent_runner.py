"""
AGENT RUNNER (MCP + AUTO TOOL DISCOVERY)

Flow:
User → LLM → Discover Tools → Choose Action → Call MCP Server → Final Answer
"""

from langchain_community.chat_models import ChatOllama
import requests

# 🔹 STEP 1: Load Agent Prompt
def load_agent_prompt():
    with open("agent/agent_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

# 🔹 STEP 2: Initialize LLM
llm = ChatOllama(model="mistral")

# 🔹 STEP 3: Get available tools from MCP server
def get_available_tools():
    try:
        response = requests.get("http://localhost:5000/tools", timeout=10)
        data = response.json()
        return data.get("tools", [])
    except Exception:
        return []

# 🔹 STEP 4: Call MCP tool
def call_tool(tool_name, tool_input):
    try:
        response = requests.post(
            "http://localhost:5000/execute",
            json={"tool": tool_name, "input": tool_input},
            timeout=30
        )
        data = response.json()

        if "result" in data:
            return data["result"]
        return data.get("error", "Unknown tool error")

    except Exception as e:
        return f"Connection error: {str(e)}"

# 🔹 STEP 5: Run Agent
def run_agent(user_query: str):

    agent_prompt = load_agent_prompt()

    # 🔹 Fetch tools dynamically
    tools = get_available_tools()

    tool_descriptions = "\n".join([
        f"{tool['name']}: {tool['description']}"
        for tool in tools
    ])

    # 🔹 Build prompt with tools injected
    full_prompt = f"""
{agent_prompt}

AVAILABLE TOOLS:
{tool_descriptions}

User Question:
{user_query}
"""

    # 🔹 LLM decides action
    response = llm.invoke(full_prompt)
    output = response.content

    print("\n🧠 Agent Raw Output:\n", output)

    # 🔹 Parse action
    action = None
    action_input = None

    for line in output.split("\n"):
        if line.startswith("Action:"):
            action = line.replace("Action:", "").strip()
        if line.startswith("Action Input:"):
            action_input = line.replace("Action Input:", "").strip()

    # 🔹 Execute tool via MCP
    observation = "None"

    if action and action != "None":
        observation = call_tool(action, action_input)

    print("\n🔧 Observation:\n", observation)

    # 🔹 Final answer
    final_prompt = f"""
{agent_prompt}

User Question:
{user_query}

Tool Observation:
{observation}

Now generate FINAL ANSWER.
"""


# 🔹 STEP 6: Loop
if __name__ == "__main__":
    while True:
        query = input("\nAsk your question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        run_agent(query)