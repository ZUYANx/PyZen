PyZen

Lightweight Local AI Runtime for Tool Calling

PyZen is a lightweight Python runtime designed to connect local AI models with real application tools.

It provides a simple developer-facing API for building local AI applications that can understand user requests, extract structured arguments, select tools, and execute Python functions without requiring a cloud AI API.

Repository: "github.com/ZUYANX/PyZen" (https://github.com/ZUYANX/PyZen)

---

Overview

PyZen is designed around a simple idea:

«Give a small local model access to real application functions.»

For example, an application can expose:

def check_orders(phone: str):
    return {
        "phone": phone,
        "count": 3
    }

A user can then ask:

01837478xxx er koyta order ache?

PyZen can identify the required tool and produce:

{
  "name": "check_orders",
  "arguments": {
    "phone": "01837478xxx"
  }
}

The application can then execute the function locally.

---

Why PyZen?

PyZen focuses on:

- Local inference
- Low memory usage
- Tool calling
- Structured arguments
- Python integration
- Android and Termux support
- Offline-capable application architecture
- Simple developer API
- Minimal runtime overhead

The goal is to make local AI practical for small applications, automation systems, bots, utilities, and embedded workflows.

---

Architecture

                    User Request
                         |
                         v
                +----------------+
                |     PyZen      |
                | Python API     |
                +-------+--------+
                        |
                        v
                +----------------+
                | Tool Registry  |
                +-------+--------+
                        |
                        v
                +----------------+
                | Native Runtime |
                +-------+--------+
                        |
                        v
                +----------------+
                | Local AI Model |
                +-------+--------+
                        |
                        v
                 Function Call
                        |
                        v
                +----------------+
                | Python Tool    |
                | / Application  |
                +----------------+

---

Features

Local AI

PyZen is designed to run AI inference locally instead of sending application data to a remote AI service.

Tool Calling

Register normal Python functions as tools.

from pyzen import PyZen, ToolRegistry

registry = ToolRegistry()


@registry.tool
def check_orders(phone: str):
    return {
        "phone": phone,
        "count": 3
    }


ai = PyZen(
    "models/needle2.cact",
    tools=registry
)

result = ai.auto_execute(
    "01837478901 er koyta order ache?"
)

print(result)

Example result:

{
    "model": {
        "type": "call",
        "function_calls": [
            {
                "name": "check_orders",
                "arguments": {
                    "phone": "0183740xx1"
                }
            }
        ]
    },
    "executed": [
        {
            "name": "check_orders",
            "arguments": {
                "phone": "018374xxx1"
            },
            "result": {
                "phone": "018374xxx",
                "count": 3
            }
        }
    ]
}

---

Installation

Clone the Repository

git clone https://github.com/ZUYANX/PyZen.git
cd PyZen

Install PyZen in editable mode:

python -m pip install -e .

Verify the installation:

python -c "import pyzen; print(pyzen.__version__)"

Expected:

0.1.0

---

Android / Termux

PyZen can run on Android through Termux using the Android ARM64 native runtime.

Install Requirements

pkg update
pkg install python git curl

Create a virtual environment:

python -m venv ~/needle-env
source ~/needle-env/bin/activate

Install the Python package:

python -m pip install cactus-needle

---

Download the Native Runtime

Create the PyZen engine directory:

mkdir -p ~/.pyzen/engine

Download the Android ARM64 runtime:

needle download android-arm64 --generation 2 --out ~/.pyzen/engine

Create a local executable directory:

mkdir -p ~/.local/bin

Copy the runtime:

cp ~/.pyzen/engine/android-arm64/needle ~/.local/bin/needle-native

Make it executable:

chmod +x ~/.local/bin/needle-native

Add it to PATH.

For Bash:

export PATH="$HOME/.local/bin:$PATH"

For Fish:

set -Ux fish_user_paths $HOME/.local/bin $fish_user_paths

Verify:

needle-native --help

---

Model

PyZen's current backend is based on the Needle 2 native engine.

Download the model:

mkdir -p models
curl -L https://huggingface.co/Cactus-Compute/needle2/resolve/main/needle2.cact -o models/needle2.cact

Verify the SHA-256 checksum:

sha256sum models/needle2.cact

Expected checksum:

b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba

The model should be stored at:

PyZen/
└── models/
    └── needle2.cact

---

Configure the Engine

PyZen can use the "PYZEN_ENGINE" environment variable to locate the native runtime.

For Bash:

export PYZEN_ENGINE="$HOME/.local/bin/needle-native"

For Fish:

set -Ux PYZEN_ENGINE "$HOME/.local/bin/needle-native"

Verify:

echo $PYZEN_ENGINE

---

Basic Usage

from pyzen import PyZen

ai = PyZen("models/needle2.cact")

response = ai(
    "Hello, what can you do?"
)

print(response)

---

Tool Calling

The main PyZen workflow is registering application functions.

from pyzen import PyZen, ToolRegistry

registry = ToolRegistry()


@registry.tool
def check_orders(phone: str):
    return {
        "phone": phone,
        "count": 3
    }


ai = PyZen(
    "models/needle2.cact",
    tools=registry
)

response = ai(
    "01837xxxx1 er koyta order ache?"
)

print(response)

The model can identify:

{
  "name": "check_orders",
  "arguments": {
    "phone": "01837xxxx1"
  }
}

---

Automatic Tool Execution

PyZen also provides "auto_execute()".

from pyzen import PyZen, ToolRegistry

registry = ToolRegistry()


@registry.tool
def check_orders(phone: str):
    return {
        "phone": phone,
        "count": 3
    }


ai = PyZen(
    "models/needle2.cact",
    tools=registry
)

result = ai.auto_execute(
    "01837xxxxx er koyta order ache?"
)

print(result)

This performs:

User request
      |
      v
Model inference
      |
      v
Tool selection
      |
      v
Argument extraction
      |
      v
Python function execution
      |
      v
Tool result

---

Creating Custom Tools

Any suitable Python function can be exposed through the registry.

from pyzen import ToolRegistry

registry = ToolRegistry()


@registry.tool
def get_customer(name: str):
    return {
        "name": name,
        "status": "active"
    }


@registry.tool
def calculate_total(price: float, quantity: int):
    return price * quantity

PyZen generates tool schemas from the Python function signatures and type hints.

---

Real-World Example

PyZen can be connected to an existing application.

For example:

from pyzen import PyZen, ToolRegistry

registry = ToolRegistry()


@registry.tool
def get_order_status(order_id: str):
    # Connect this to your database or API.
    return {
        "order_id": order_id,
        "status": "processing"
    }


@registry.tool
def check_orders(phone: str):
    # Replace with your real database query.
    return {
        "phone": phone,
        "count": 3
    }


ai = PyZen(
    "models/needle2.cact",
    tools=registry
)

result = ai.auto_execute(
    "0183xxxxxx1 er koyta order ache?"
)

print(result)

This allows PyZen to act as a lightweight AI layer on top of an existing application.

---

Supported Platforms

The current native runtime architecture is intended to support:

Platform| Architecture
Android| ARM64
Android| ARMv7
Android| RISC-V
Linux| ARM64
Linux| x86_64
macOS| ARM64
Windows| ARM64
Windows| x86_64
WebAssembly| WASM

Actual availability depends on the native runtime binaries provided by the underlying engine.

---

Linux

Install the runtime package:

python -m pip install cactus-needle

Download an ARM64 runtime:

needle download linux-arm64 --generation 2 --out ~/.pyzen/engine

Or download an x86_64 runtime when available:

needle download linux-x86_64 --generation 2 --out ~/.pyzen/engine

Configure PyZen:

export PYZEN_ENGINE="$HOME/.pyzen/engine/linux-arm64/needle"

Verify:

"$PYZEN_ENGINE" --help

---

macOS

Install:

python -m pip install cactus-needle

Download the ARM64 runtime:

needle download macos-arm64 --generation 2 --out ~/.pyzen/engine

Configure:

export PYZEN_ENGINE="$HOME/.pyzen/engine/macos-arm64/needle"

Verify:

"$PYZEN_ENGINE" --help

---

Windows

Install the Python package:

python -m pip install cactus-needle

Download the runtime:

needle download windows-arm64 --generation 2 --out "$HOME\.pyzen\engine"

For x86_64 systems, use the corresponding Windows x86_64 runtime.

Configure PowerShell:

$env:PYZEN_ENGINE="$HOME\.pyzen\engine\windows-arm64\needle.exe"

Verify:

& $env:PYZEN_ENGINE --help

---

Environment Variables

Variable| Purpose
"PYZEN_ENGINE"| Path to the native PyZen/Needle runtime

Example:

export PYZEN_ENGINE="$HOME/.local/bin/needle-native"

---

Project Structure

PyZen/
│
├── pyzen/
│   ├── __init__.py
│   ├── cli.py
│   ├── model.py
│   ├── runtime.py
│   ├── runtime_ctypes.py
│   └── tools.py
│
├── examples/
│   └── order_demo.py
│
├── tests/
│   └── test_tools.py
│
├── models/
│   ├── README.txt
│   └── needle2.cact
│
├── native/
│   └── README.txt
│
├── scripts/
│   └── install_termux.fish
│
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml

---

Core API

"PyZen"

Main interface for local AI inference.

from pyzen import PyZen

ai = PyZen("models/needle2.cact")

"ToolRegistry"

Manages application tools.

from pyzen import ToolRegistry

registry = ToolRegistry()

"tool"

Register Python functions as AI-callable tools.

@registry.tool
def check_orders(phone: str):
    return {"count": 3}

"complete"

Run model inference.

response = ai.complete(
    "01837xxxx1 er koyta order ache?"
)

"auto_execute"

Run inference and execute returned tool calls.

result = ai.auto_execute(
    "01837xxxxx1 er koyta order ache?"
)

---

CLI

PyZen also exposes a command-line entry point.

After installation:

pyzen --help

The CLI interface is intended to provide a simple way to interact with the runtime without writing a complete Python application.

---

Testing

Run the test suite:

python -m pytest -q

Expected:

1 passed

Run the example:

python examples/order_demo.py

---

Performance

The current Android prototype has demonstrated:

Peak RAM: approximately 23–24 MB

Inference speed varies depending on device, runtime version, prompt, and execution environment.

Example Android measurements have reached roughly:

Prefill: ~280–290 tokens/sec
Decode:  ~100–140 tokens/sec

These numbers are examples from development hardware and should not be treated as guaranteed benchmarks.

---

Privacy

PyZen is designed around local inference.

Application data can remain inside the device or server running the runtime instead of being automatically sent to a cloud AI provider.

However, privacy depends on the application and tools connected to PyZen. A tool that calls an external API can naturally send data to that API.

Developers should review all registered tools before deploying PyZen in privacy-sensitive environments.

---

Security

PyZen tools execute Python functions provided by the application.

Only expose functions that the application is intentionally allowing the AI to call.

For production applications:

- Validate tool arguments.
- Authenticate sensitive operations.
- Authorize users before performing protected actions.
- Avoid exposing unrestricted shell execution.
- Avoid passing secrets directly into model prompts.
- Log important tool operations.
- Handle tool failures safely.
- Apply rate limits where appropriate.

For example, avoid exposing unrestricted functions such as:

@registry.tool
def execute_command(command: str):
    ...

unless the application has a carefully designed security boundary around it.

---

Current Runtime Design

The current PyZen 0.1 runtime uses a native subprocess backend.

Conceptually:

Python Application
       |
       v
     PyZen
       |
       v
 ToolRegistry
       |
       v
 Native Runtime
       |
       v
 Local Model

The Python layer handles the developer API and tool registration while the native runtime performs model inference.

The current standalone native runner uses its own embedded/base model integration. The ".cact" model file is retained as part of PyZen's model-management architecture and for future backend support.

---

Development Status

PyZen is currently in early development.

PyZen 0.1

Implemented:

- Python package
- "PyZen" API
- "ToolRegistry"
- Function schema generation
- Tool calling
- Structured arguments
- Native subprocess runtime
- Android ARM64 runtime
- Termux support
- Automatic tool execution
- Basic tests
- Example application

---

Roadmap

Planned improvements include:

Runtime

- Native backend abstraction
- Better ".cact" model loading
- Runtime version management
- Cross-platform packaging
- WASM support
- More efficient process management

AI

- Tool result to final-answer loop
- Multiple tool calls
- Conversation state
- Streaming inference
- Better structured output handling
- Improved error recovery

Developer Experience

- Cleaner configuration
- CLI improvements
- Automatic runtime installation
- Better diagnostics
- Type-safe APIs
- Documentation
- PyPI distribution

Ecosystem

- Plugin architecture
- Database integrations
- HTTP API integration
- Telegram bot integration
- E-commerce integrations
- Automation workflows
- Embedded AI applications

---

Example Use Cases

PyZen can be integrated into applications such as:

E-commerce
      |
      +-- Order lookup
      +-- Customer lookup
      +-- Product search
      +-- Stock checking

Automation
      |
      +-- Task execution
      +-- Data processing
      +-- API calls

Bots
      |
      +-- Telegram bots
      +-- Customer support
      +-- Business assistants

Developer Tools
      |
      +-- Local coding assistants
      +-- CLI utilities
      +-- Structured command systems

Embedded AI
      |
      +-- Android applications
      +-- Edge devices
      +-- Offline utilities

---

Contributing

Contributions are welcome.

Fork the repository:

git clone https://github.com/ZUYANX/PyZen.git
cd PyZen

Create a branch:

git checkout -b feature/my-feature

Install development dependencies:

python -m pip install -e .

Run tests:

python -m pytest -q

Commit your changes:

git add .
git commit -m "Add new feature"

Push the branch:

git push origin feature/my-feature

Then open a pull request on GitHub.

---

License

See the "LICENSE" file for the project's license.

PyZen's Python code, native runtime, and model files may have different licensing terms depending on their source. Review the relevant upstream licenses before redistributing third-party components.

---

Author

MR ZUYAN

GitHub:

https://github.com/ZUYANX

Project:

https://github.com/ZUYANX/PyZen

---

Project Philosophy

PyZen is built around a simple principle:

Small Model
    +
Simple Runtime
    +
Real Tools
    =
Useful Local AI

The objective is not to build another cloud chatbot.

The objective is to make small local models useful inside real software.

---

PyZen — Local AI, connected to your tools.
