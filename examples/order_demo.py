from pyzen import PyZen, ToolRegistry

registry = ToolRegistry()

def check_orders(phone: str):
    """Check how many orders belong to a phone number.""" 
    return {"phone": phone, "count": 3}

registry.register(check_orders)

ai = PyZen(
    model_path="models/needle2.cact",
    engine_path=None,
    tools=registry,
)

result = ai.auto_execute("01837478901 er koyta order ache?")
print(result)
