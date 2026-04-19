# Simple in-memory store (can later replace with DB / vector store)

memory_store = []


def save_memory(user_input, plan, result):
    memory_store.append({
        "input": user_input,
        "plan": plan,
        "result": result
    })


def get_memory():
    return memory_store


def last_memory():
    if memory_store:
        return memory_store[-1]
    return None