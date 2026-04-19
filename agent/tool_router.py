from tools.api_test import api_test

TOOLS = {
    "api_test": api_test
}


def execute_tool(plan):
    tool_name = plan.get("tool")

    if tool_name not in TOOLS:
        return {"error": "Tool not found"}

    tool = TOOLS[tool_name]

    payload = {
        "method": plan.get("method"),
        "url": plan.get("url"),
        "payload": plan.get("payload", {})
    }

    # IMPORTANT FIX: already dict → no need to stringify
    return tool(payload)