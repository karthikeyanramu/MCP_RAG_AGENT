"""ULTRA FAST API AGENT (IMPROVED METHOD MAPPING + LOGGING)

This module parses user intents into API calls, selects appropriate
HTTP methods, and routes requests through the local MCP tool server.
"""

import json
import re
import os
import requests
from qa_agent.report_generator import generate_html_report

# Load configuration (endpoints, base_url)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "api_config.json")

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        API_CONFIG = json.load(fh)
except Exception:
    API_CONFIG = {"base_url": "https://reqres.in", "endpoints": {}}

BASE_URL = API_CONFIG.get("base_url", "https://reqres.in")


def _choose_update_method(user_query: str):
    q = user_query.lower()
    if "patch" in q or "partial" in q:
        return "PATCH"
    return "PUT"


def parse_user_input(user_query: str) -> dict:
    """Parse the user query and return a payload describing method, url, payload.

    The parser is permissive to verbs: create -> POST, get/retrieve -> GET,
    update -> PUT/PATCH (choose PATCH if 'patch' or 'partial' present), delete -> DELETE.
    """

    uq = user_query.lower().strip()

    # GET / Retrieve
    if match := re.search(r"(?:get|retrieve) user (\d+)", uq):
        user_id = match.group(1)
        return {"method": "GET", "url": f"{BASE_URL}/api/users/{user_id}"}

    # List users by page
    if match := re.search(r"list users(?: page)? (\d+)", uq):
        page = match.group(1)
        return {"method": "GET", "url": f"{BASE_URL}/api/users?page={page}"}

    # Create
    if "create" in uq:
        # Try to infer body fields from the query (very simple)
        payload = {"name": "test", "job": "qa"}
        return {"method": "POST", "url": f"{BASE_URL}/api/users", "payload": payload}

    # Update (PUT or PATCH)
    if match := re.search(r"(?:update|modify) user (\d+)", uq):
        user_id = match.group(1)
        method = _choose_update_method(uq)
        payload = {"name": "updated", "job": "lead qa"} if method == "PUT" else {"job": "patched qa"}
        return {"method": method, "url": f"{BASE_URL}/api/users/{user_id}", "payload": payload}

    # Explicit patch phrasing
    if match := re.search(r"patch user (\d+)", uq):
        user_id = match.group(1)
        return {"method": "PATCH", "url": f"{BASE_URL}/api/users/{user_id}", "payload": {"job": "patched qa"}}

    # Delete
    if match := re.search(r"delete user (\d+)", uq):
        user_id = match.group(1)
        return {"method": "DELETE", "url": f"{BASE_URL}/api/users/{user_id}"}

    # Fallback: return a helpful unknown endpoint
    return {"method": "GET", "url": f"{BASE_URL}/api/unknown/999"}


# -----------------------------
# MCP CALL
# -----------------------------
def call_api_tool(payload):

    response = requests.post(
        "http://localhost:5000/execute",
        json={
            "tool": "api_test",
            "input": json.dumps(payload)
        },
        timeout=30
    )

    data = response.json()

    result = data.get("result", data)

    # The MCP tool often returns a JSON string in 'result'. Normalize it here.
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return result

    return result


# -----------------------------
# NORMALIZER
# -----------------------------
def normalize_response(observation):

    if isinstance(observation, str):
        try:
            return json.loads(observation)
        except:
            return {"error": "Invalid JSON"}

    return observation


# -----------------------------
# VALIDATION
# -----------------------------
def validate_response(observation):

    if isinstance(observation, dict) and "error" in observation:
        return "FAIL", observation["error"]

    status_code = observation.get("status_code", 0)

    if 200 <= status_code < 300:
        return "PASS", f"Valid response ({status_code})"

    return "FAIL", f"Unexpected status code: {status_code}"


# -----------------------------
# RUNNER
# -----------------------------
def run_api_agent(user_query):


    print(f"\n🧠 Query: {user_query}")

    parsed = parse_user_input(user_query)

    method_selected = parsed.get("method")
    url = parsed.get("url")
    payload_body = parsed.get("payload", {})

    # Build final payload for the MCP tool
    payload = {
        "method": method_selected,
        "url": url,
        "payload": payload_body,
        "auth_required": True
    }

    # LOGGING (important for traceability)
    print("\n🔎 Selected HTTP method:", method_selected)
    print("🔗 Endpoint:", url)
    print("📝 Input action:", user_query)
    print("📦 Request payload:", json.dumps(payload_body, indent=2))

    raw_response = call_api_tool(payload)

    observation = normalize_response(raw_response)

    # Response logging
    try:
        status_code = observation.get("status_code", "N/A")
        body = observation.get("response_body", observation)
    except Exception:
        status_code = "N/A"
        body = observation

    print("\n📤 Response status:", status_code)
    try:
        print("📥 Response body:", json.dumps(body, indent=2))
    except Exception:
        print("📥 Response body:", body)

    status, message = validate_response(observation)

    print(f"\n✅ RESULT: {status} - {message}")

    report_file = generate_html_report(
        user_query=user_query,
        response=observation,
        status=status,
        message=message
    )

    print(f"\n📄 REPORT: {report_file}")


if __name__ == "__main__":

    while True:
        query = input("\nAsk API test (exit to quit): ")

        if query.lower() == "exit":
            break

        run_api_agent(query)