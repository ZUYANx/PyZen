import inspect
import json
from typing import Any, Callable, Dict, List, Optional, get_type_hints

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register(self, fn: Callable[..., Any], name: Optional[str] = None,
                 description: Optional[str] = None):
        tool_name = name or fn.__name__
        self._tools[tool_name] = fn
        return fn

    def get(self, name: str):
        return self._tools[name]

    def functions(self) -> List[Callable[..., Any]]:
        return list(self._tools.values())

    def schemas(self) -> List[dict]:
        result = []
        for fn in self.functions():
            sig = inspect.signature(fn)
            hints = get_type_hints(fn)
            props = {}
            required = []
            for pname, param in sig.parameters.items():
                if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    continue
                typ = hints.get(pname, str)
                typ_name = getattr(typ, "__name__", "string")
                json_type = {
                    "str": "string", "int": "integer", "float": "number",
                    "bool": "boolean", "dict": "object", "list": "array"
                }.get(typ_name, "string")
                props[pname] = {"type": json_type}
                if param.default is inspect.Parameter.empty:
                    required.append(pname)
            result.append({
                "name": fn.__name__,
                "description": inspect.getdoc(fn) or "",
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required
                }
            })
        return result

    def json(self) -> str:
        return json.dumps(self.schemas(), ensure_ascii=False, separators=(",", ":"))

    def execute(self, name: str, arguments: dict):
        return self.get(name)(**arguments)

def tool(fn=None, *, name=None, description=None, registry=None):
    reg = registry or _default_registry
    def decorator(func):
        return reg.register(func, name=name, description=description)
    return decorator(fn) if fn else decorator

_default_registry = ToolRegistry()
