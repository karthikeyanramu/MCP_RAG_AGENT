"""
API TESTING TOOL (PRODUCTION STABLE - FIXED HTTP METHOD HANDLING)
"""

import requests
import json
import time
import traceback

API_KEY = "pub_b27ca8191d68e08569db9f9fa7637fb373632c9780eea34724c0c63a1544c5e0"

ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def api_test(input_data: str) -> str:

    try:
        data = json.loads(input_data)

        method = str(data.get("method", "")).upper().strip()
        url = data.get("url")
        payload = data.get("payload", {}) or {}
        headers_in = data.get("headers", {}) or {}

        auth_required = data.get("auth_required", True)
        auth_type = data.get("auth_type", "api_key")

        # -----------------------------
        # VALIDATION (FIX #1)
        # -----------------------------
        if not url:
            return json.dumps({"error": "URL is required"})

        if method not in ALLOWED_METHODS:
            return json.dumps({
                "error": f"Invalid HTTP method: {method}. Allowed: {ALLOWED_METHODS}"
            })

        # -----------------------------
        # BASE HEADERS
        # -----------------------------
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.36.0"
        }

        # -----------------------------
        # AUTH
        # -----------------------------
        if auth_required:

            if auth_type == "api_key":
                headers["x-api-key"] = API_KEY

            elif auth_type == "bearer":
                headers["Authorization"] = f"Bearer {API_KEY}"

            elif auth_type != "none":
                return json.dumps({"error": "Invalid auth_type"})

        headers.update(headers_in)

        # -----------------------------
        # DEBUG (IMPORTANT)
        # -----------------------------
        print("\n🔍 FINAL REQUEST DEBUG")
        print("METHOD:", method)
        print("URL:", url)
        print("HEADERS:", headers)
        print("PAYLOAD:", payload)

        start_time = time.time()

        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload if method in ["POST", "PUT", "PATCH"] else None,
                params=payload if method == "GET" else None,
                headers=headers,
                timeout=5
            )

        except requests.exceptions.Timeout:
            return json.dumps({"error": "Timeout after retry"})

        response_time = round((time.time() - start_time) * 1000, 2)

        try:
            body = response.json()
        except:
            body = response.text

        return json.dumps({
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "response_body": body,
            "method_executed": method,   # 🔥 IMPORTANT DEBUG FIELD
            "url": url
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "trace": traceback.format_exc()
        }, indent=2)