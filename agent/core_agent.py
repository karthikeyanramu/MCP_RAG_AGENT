from agent.planner import llm_plan
from agent.tool_router import execute_tool
from agent.memory import save_memory, get_memory


def run_agent(user_input):

    print("\n🧠 USER INPUT:", user_input)

    # STEP 1: PLAN
    plan = llm_plan(user_input)
    print("\n📌 PLAN:", plan)

    # STEP 2: EXECUTE TOOL
    result = execute_tool(plan)
    print("\n🔧 RESULT:", result)

    # STEP 3: MEMORY SAVE
    save_memory(user_input, plan, result)

    return result


# -----------------------------
# Interactive Agent Loop
# -----------------------------
if __name__ == "__main__":

    print("\n🤖 MCP AGENT STARTED (type 'exit' to stop)\n")

    while True:
        user_input = input("Ask: ")

        if user_input.lower() == "exit":
            break

        run_agent(user_input)

    print("\n🧠 MEMORY SNAPSHOT:")
    print(get_memory())