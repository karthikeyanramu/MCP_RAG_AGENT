"""
TOOL REGISTRY

Purpose:
Acts as a central place where all tools are registered.

Why:
Instead of hardcoding tool calls in the agent,
the agent can dynamically discover tools.

This is the first step toward MCP-style architecture.
"""

from tools.rag_tool import knowledge_search
from tools.calculator_tool import calculator

# Dictionary of available tools
TOOLS = {
    "knowledge_search": knowledge_search,
    "calculator": calculator
}


def get_tool(tool_name):
    """
    Return the tool function based on tool name
    """
    return TOOLS.get(tool_name)