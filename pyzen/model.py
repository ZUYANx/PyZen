import json
import os
from pathlib import Path
from .runtime import NativeRuntime
from .tools import ToolRegistry

class PyZen:
    """Small tool-calling AI runtime with a clean PyZen API."""

    def __init__(self, model_path="models/needle2.cact", engine_path=None,
                 tools=None, system_prompt=None):
        base = Path(__file__).resolve().parent.parent
        self.model_path = str(Path(model_path).expanduser())
        if not os.path.isabs(self.model_path):
            self.model_path = str(base / self.model_path)

        engine_path = engine_path or os.environ.get("PYZEN_ENGINE")
        if not engine_path:
            engine_path = os.path.join(os.environ.get("PREFIX", ""), "bin", "needle-native")

        self.registry = tools or ToolRegistry()
        self.runtime = NativeRuntime(engine_path, self.model_path)
        self.system_prompt = system_prompt
        self.runtime.init(system_prompt, self.registry.json())

    def tool(self, fn=None, *, name=None, description=None):
        def decorator(func):
            self.registry.register(func, name=name, description=description)
            self.runtime.init(self.system_prompt, self.registry.json())
            return func
        return decorator(fn) if fn else decorator

    def complete(self, prompt: str, max_new_tokens=256):
        return self.runtime.complete(prompt, max_new_tokens)

    def __call__(self, prompt: str, max_new_tokens=256):
        raw = self.complete(prompt, max_new_tokens)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def auto_execute(self, prompt: str, max_new_tokens=256):
        result = self(prompt, max_new_tokens)
        if not isinstance(result, dict):
            return result
        calls = result.get("function_calls") or []
        if not calls:
            return result

        executed = []
        for call in calls:
            name = call["name"]
            args = call.get("arguments") or {}
            value = self.registry.execute(name, args)
            executed.append({
                "name": name,
                "arguments": args,
                "result": value
            })
        return {"model": result, "executed": executed}
