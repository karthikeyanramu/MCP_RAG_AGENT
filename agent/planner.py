def llm_plan(user_input):
    """
    Simulated planner (later replace with LLM like OpenAI / GPT)
    """

    text = user_input.lower()

    if "create user" in text:
        return {
            "tool": "api_test",
            "method": "POST",
            "url": "https://reqres.in/api/users",
            "payload": {"name": "test", "job": "qa"}
        }

    if "get user" in text:
        return {
            "tool": "api_test",
            "method": "GET",
            "url": "https://reqres.in/api/users/2",
            "payload": {}
        }

    if "delete user" in text:
        return {
            "tool": "api_test",
            "method": "DELETE",
            "url": "https://reqres.in/api/users/2",
            "payload": {}
        }

    return {
        "tool": "api_test",
        "method": "GET",
        "url": "https://reqres.in/api/unknown",
        "payload": {}
    }