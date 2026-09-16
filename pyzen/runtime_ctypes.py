import ctypes
import json
import os
from pathlib import Path
from typing import Optional

class NativeRuntime:
    """Thin ctypes wrapper around the Android ARM64 Needle 2 C API.

    PyZen owns the public API; this class is the private native backend.
    """
    def __init__(self, engine_path: str, model_path: str):
        self.engine_path = str(engine_path)
        self.model_path = str(model_path)
        self.lib = ctypes.CDLL(self.engine_path)

        self.lib.needle_load.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int]
        self.lib.needle_load.restype = ctypes.c_int

        self.lib.needle_init.argtypes = [
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
        ]
        self.lib.needle_init.restype = ctypes.c_int

        self.lib.needle_complete.argtypes = [
            ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
        ]
        self.lib.needle_complete.restype = ctypes.c_int

        self.lib.needle_reset.argtypes = []
        self.lib.needle_reset.restype = None

        self._load_model()

    def _load_model(self):
        data = Path(self.model_path).read_bytes()
        buf = (ctypes.c_uint8 * len(data)).from_buffer_copy(data)
        rc = self.lib.needle_load(buf, len(data))
        if rc != 0:
            raise RuntimeError(f"needle_load failed: {rc}")

    def init(self, system_prompt: Optional[str] = None,
             tools_json: Optional[str] = None,
             tool_index_path: Optional[str] = None):
        def enc(x):
            return x.encode() if x is not None else None
        rc = self.lib.needle_init(enc(system_prompt), enc(tools_json),
                                  enc(tool_index_path))
        if rc < 0:
            raise RuntimeError(f"needle_init failed: {rc}")
        return rc

    def complete(self, prompt: str, max_new_tokens: int = 256) -> str:
        # Large fixed buffer keeps the wrapper simple for the first release.
        size = max(16_384, max_new_tokens * 4096)
        out = ctypes.create_string_buffer(size)
        rc = self.lib.needle_complete(
            prompt.encode("utf-8"), max_new_tokens, out, size
        )
        if rc < 0:
            raise RuntimeError(f"needle_complete failed: {rc}")
        return out.value.decode("utf-8", errors="replace")

    def reset(self):
        self.lib.needle_reset()
