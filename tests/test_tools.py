from pyzen.tools import ToolRegistry

def test_schema_and_execution():
    r = ToolRegistry()

    def add(a: int, b: int):
        return a + b

    r.register(add)
    schema = r.schemas()[0]
    assert schema["name"] == "add"
    assert schema["parameters"]["required"] == ["a", "b"]
    assert r.execute("add", {"a": 2, "b": 3}) == 5
