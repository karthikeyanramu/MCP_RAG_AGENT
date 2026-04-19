"""
CALCULATOR TOOL

Simple tool for math operations
"""

def calculator(expression: str) -> str:
    """
    TOOL: calculator

    Input:
        expression (str) → e.g. "25 * 4"

    Output:
        str → result
    """

    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid mathematical expression"