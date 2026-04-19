"""Small CLI wrapper to exercise the API agent from command line.

Usage:
    python -m qa_agent.api_test_agent

It reads simple commands like "create user", "get user 2", "update user 3", etc.
"""

from qa_agent.api_agent_runner import run_api_agent


def main():
    print("API Test Agent - type 'exit' to quit")
    while True:
        q = input("\nAction: ")
        if not q:
            continue
        if q.lower().strip() == "exit":
            break
        run_api_agent(q)


if __name__ == "__main__":
    main()
