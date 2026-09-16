import json
import os
import subprocess
from pathlib import Path

class NativeRuntime:
    def __init__(self, engine_path=None, model_path=None):
        self.engine_path = engine_path or os.environ.get(
            "PYZEN_ENGINE", os.path.expandvars("$PREFIX/bin/needle-native")
        )
        self.model_path = str(Path(model_path).expanduser()) if model_path else None

        if not os.path.isfile(self.engine_path):
            raise FileNotFoundError(f"Native engine not found: {self.engine_path}")
        if self.model_path and not os.path.isfile(self.model_path):
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        self.tools_json = None
        self.system_prompt = None
        self.tool_index_path = None

    def init(self, system_prompt=None, tools_json=None, tool_index_path=None):
        self.system_prompt = system_prompt
        self.tools_json = tools_json
        self.tool_index_path = tool_index_path
        return 0

    def complete(self, prompt, max_new_tokens=256):
        if not self.model_path:
            raise RuntimeError("model_path is required")

        cmd = [self.engine_path]

        if self.tools_json:
            import tempfile
            fd, tools_path = tempfile.mkstemp(suffix=".json")
            os.close(fd)
            Path(tools_path).write_text(self.tools_json)
            cmd += ["--tools", tools_path]

        if self.system_prompt:
            cmd += ["--system", self.system_prompt]

        cmd += ["--max", str(max_new_tokens), "--prompt", prompt]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
        finally:
            if self.tools_json:
                try:
                    os.unlink(tools_path)
                except Exception:
                    pass

        if result.returncode != 0:
            raise RuntimeError(
                f"needle-native failed ({result.returncode}): {result.stderr.strip()}"
            )

        output = result.stdout.strip()
        if not output:
            raise RuntimeError("needle-native returned empty output")

        return output

    def reset(self):
        # CLI mode is stateless per invocation.
        return None
