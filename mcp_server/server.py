"""
MCP-STYLE TOOL SERVER (PRODUCTION-STABLE VERSION)
"""

from flask import Flask, request, jsonify
import sys
import os
import json
import logging
import traceback

# -----------------------------
# PATH FIX
# -----------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------
# TOOL IMPORTS
# -----------------------------
from tools.rag_tool import knowledge_search
from tools.calculator_tool import calculator
from tools.api_tool import api_test

# -----------------------------
# APP INIT
# -----------------------------
app = Flask(__name__)

# -----------------------------
# LOGGING CONFIG (IMPORTANT UPGRADE)
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------
# TOOL REGISTRY
# -----------------------------
TOOLS = {
    "knowledge_search": {
        "function": knowledge_search,
        "description": "Search internal knowledge base"
    },
    "calculator": {
        "function": calculator,
        "description": "Perform mathematical calculations"
    },
    "api_test": {
        "function": api_test,
        "description": "Execute API requests with validation and auth support"
    }
}


# -----------------------------
# HEALTH CHECK (NEW - BEST PRACTICE)
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "tools_loaded": list(TOOLS.keys())
    })


# -----------------------------
# LIST TOOLS
# -----------------------------
@app.route("/tools", methods=["GET"])
def list_tools():
    return jsonify({
        "tools": [
            {
                "name": name,
                "description": data["description"]
            }
            for name, data in TOOLS.items()
        ]
    })


# -----------------------------
# EXECUTE TOOL
# -----------------------------
@app.route("/execute", methods=["POST"])
def execute_tool():

    try:
        data = request.json or {}

        tool_name = data.get("tool")
        tool_input = data.get("input")

        logging.info(f"Tool Requested: {tool_name}")
        logging.info(f"Input Received: {tool_input}")

        # -----------------------------
        # VALIDATION
        # -----------------------------
        if not tool_name:
            return jsonify({"error": "tool is required"}), 400

        if tool_name not in TOOLS:
            return jsonify({
                "error": "Tool not found",
                "available_tools": list(TOOLS.keys())
            }), 404

        if tool_input is None:
            return jsonify({"error": "input is required"}), 400

        # -----------------------------
        # NORMALIZE INPUT (CRITICAL FIX)
        # -----------------------------
        if isinstance(tool_input, dict):
            tool_input = json.dumps(tool_input)

        if not isinstance(tool_input, str):
            tool_input = str(tool_input)

        # Extra logging for api_test tool: method, url, payload
        if tool_name == "api_test":
            try:
                parsed = json.loads(tool_input)
                try:
                    payload_obj = json.loads(parsed) if isinstance(parsed, str) else parsed
                except Exception:
                    payload_obj = parsed

                method = payload_obj.get("method")
                url = payload_obj.get("url")
                payload = payload_obj.get("payload")

                logging.info(f"api_test -> method={method} url={url} payload={payload}")
            except Exception:
                logging.info("api_test -> could not parse input for detailed logging")

        # -----------------------------
        # EXECUTE TOOL
        # -----------------------------
        tool_function = TOOLS[tool_name]["function"]

        result = tool_function(tool_input)

        logging.info(f"Tool Execution Completed: {tool_name}")

        # -----------------------------
        # RESPONSE
        # -----------------------------
        return jsonify({
            "tool": tool_name,
            "result": result
        })

    except Exception as e:

        logging.error("Tool Execution Failed")
        logging.error(traceback.format_exc())

        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    print("🚀 MCP Server running on http://127.0.0.1:5000")
    print("🔧 Available Tools:", list(TOOLS.keys()))
    print("❤️ Health Check: http://127.0.0.1:5000/health")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )