PyZen

Lightweight Local AI Runtime for Tool Calling

PyZen is a lightweight Python runtime designed to connect compact local AI models with Python functions, APIs, databases, automation systems, and application logic.

It provides a clean application-facing API while keeping the underlying inference engine behind a runtime layer.

«Small AI. Big possibilities.»

---

What is PyZen?

PyZen allows an application to turn natural-language requests into structured tool calls.

For example:

User:
How many orders does this customer have?

PyZen can determine that the application should call:

check_orders(phone="...")

The Python function performs the actual operation.

This makes PyZen useful for:

- AI-powered APIs
- E-commerce systems
- Telegram bots
- Facebook automation
- Customer support systems
- Database assistants
- Local AI applications
- Device automation
- Lightweight agents
- Embedded AI applications

---

Core Architecture

                    User
                     |
                     v
              +-------------+
              |    PyZen    |
              +-------------+
                     |
             Natural Language
                     |
                     v
              +-------------+
              | AI Runtime  |
              +-------------+
                     |
                     v
              Native AI Engine
                     |
                     v
                Local Model
                     |
                     v
              Tool Selection
                     |
                     v
              Tool Registry
                     |
                     v
             Python Function
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Database     API      Automation

PyZen is designed so application developers do not need to directly interact with the native inference implementation.

---

Features

- Lightweight local AI runtime
- Tool calling
- Structured function arguments
- Python function execution
- Bangla and Banglish query support
- Local inference
- Low memory usage
- Native backend architecture
- Android ARM64 support
- Termux support
- Extensible tool registry
- CLI support
- Model abstraction
- Runtime abstraction
- Offline-capable architecture
- Designed for future cross-platform backends

---

Current Status

PyZen is currently an early-stage project.

The core workflow has been successfully tested on Android ARM64 through Termux.

Tested workflow:

Natural-language query
        |
        v
      PyZen
        |
        v
  Native AI engine
        |
        v
  Tool selection
        |
        v
Python function
        |
        v
Structured result

Example tested result:

{
  "name": "check_orders",
  "arguments": {
    "phone": "<customer-phone>"
  }
}

The current Android implementation uses the official Needle 2 native engine as its inference backend.

---

Requirements

General

- Python 3.9+
- Git
- pip
- A supported native inference backend
- A compatible model/runtime

Android / Termux

Recommended:

Android ARM64
Termux
Python 3.9+

The current development environment has been tested with:

Android
ARM64
Termux
Python 3.14

---

Installation

1. Clone the Repository
```bash
git clone https://github.com/ZUYANX/PyZen.git
cd PyZen
```

2. Install PyZen

Install the package in editable mode:

python -m pip install -e .

Verify:

python -c "import pyzen; print(pyzen.__version__)"

Expected:

0.1.0

---

Native Engine Setup

PyZen uses a runtime abstraction for the native inference engine.

The current tested backend is the Android ARM64 Needle 2 native engine.

The official Needle 2 distribution provides native targets for Android, Linux, Windows, macOS and other platforms.

---

Android / Termux Setup

1. Install the native engine downloader

python -m pip install cactus-needle

Verify:

needle --help

---

2. Download the Android ARM64 engine

For ARM64 Android devices:

mkdir -p ~/.pyzen/engine

needle download android-arm64 --generation 2 --out ~/.pyzen/engine

The resulting directory should contain:

~/.pyzen/engine/android-arm64/
├── needle
├── libneedle.a
└── needle.h

The official distribution provides "needle" and "libneedle.a" for Android ARM64.

---

3. Install the native runner

Create a local executable directory:

mkdir -p ~/.local/bin

Copy the Android native runner:

cp ~/.pyzen/engine/android-arm64/needle ~/.local/bin/needle-native

Make it executable:

chmod +x ~/.local/bin/needle-native

Add it to PATH if necessary:

set -Ux fish_user_paths ~/.local/bin $fish_user_paths

For Bash:

export PATH="$HOME/.local/bin:$PATH"

Verify:

needle-native --help

Expected output includes:

--prompt
--tools
--serve
--port
--max

---

Model Setup

PyZen's current model target is the official Needle 2 model:

needle2.cact

The current official model is approximately 13.7 MB.

Create the model directory:

mkdir -p models

Download the model:

curl -L \
  https://huggingface.co/Cactus-Compute/needle2/resolve/main/needle2.cact \
  -o models/needle2.cact

Verify the file:

ls -lh models/needle2.cact

Verify the official SHA256:

sha256sum models/needle2.cact

Expected SHA256:

b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba

The official model repository currently lists this SHA256 for "needle2.cact".

---

Important Model Note

The standalone native runner distributed by Needle 2 contains the base model/runtime integration required for the command-line workflow.

The "models/needle2.cact" file is kept in the PyZen project for model management, compatibility checking, and future runtime backends/custom model support.

For the current Android CLI backend, the native runner is the component actually executed by PyZen.

---

Configure the Engine

PyZen can use the environment variable:

PYZEN_ENGINE

Android / Termux:

export PYZEN_ENGINE="$HOME/.local/bin/needle-native"

Verify:

echo $PYZEN_ENGINE

Expected:

/data/data/com.termux/files/home/.local/bin/needle-native

For Fish:

set -Ux PYZEN_ENGINE "$HOME/.local/bin/needle-native"

---

First Engine Test

Run:

needle-native --help

Then test the native engine:

needle-native --prompt "Hello"

If the engine returns a structured response, the native backend is working.

---

Tool Calling

PyZen tools are normal Python functions.

Create a tool registry:

from pyzen import PyZen, ToolRegistry

registry = ToolRegistry()

Create a function:

def check_orders(phone: str):
    """Check how many orders belong to a phone number."""

    return {
        "phone": phone,
        "count": 3
    }

Register it:

registry.register(check_orders)

Create PyZen:

ai = PyZen(
    model_path="models/needle2.cact",
    tools=registry
)

Run a query:

result = ai.auto_execute(
    "How many orders does this customer have?"
)

print(result)

---

Complete Example

Create:

test.py

with:

from pyzen import PyZen, ToolRegistry


registry = ToolRegistry()


def check_orders(phone: str):
    """Check how many orders belong to a phone number."""

    return {
        "phone": phone,
        "count": 3
    }


registry.register(check_orders)


ai = PyZen(
    model_path="models/needle2.cact",
    tools=registry
)


result = ai.auto_execute(
    "How many orders does this customer have?"
)


print(result)

Run:

python test.py

The model can produce a structured tool call similar to:

{
  "function_calls": [
    {
      "name": "check_orders",
      "arguments": {
        "phone": "<customer-phone>"
      }
    }
  ]
}

PyZen then executes:

check_orders(phone="<customer-phone>")

and returns the result.

---

Using Real Database Data

PyZen does not need to know how your database works.

Your application owns the database logic.

Example:

def check_orders(phone: str):
    orders = database.find_orders_by_phone(phone)

    return {
        "phone": phone,
        "count": len(orders),
        "orders": orders
    }

This separation keeps the AI layer lightweight and the application logic under developer control.

---

Multiple Tools

You can register multiple functions:

def check_orders(phone: str):
    """Check customer orders."""
    return {"count": 3}


def get_customer(phone: str):
    """Get customer information."""
    return {
        "name": "Customer",
        "phone": phone
    }


def cancel_order(order_id: str):
    """Cancel an order."""
    return {
        "order_id": order_id,
        "status": "cancelled"
    }


registry.register(check_orders)
registry.register(get_customer)
registry.register(cancel_order)

PyZen can expose all registered tools to the model.

---

CLI Usage

PyZen provides a command-line interface.

Example:

pyzen \
  --model models/needle2.cact \
  --engine "$PYZEN_ENGINE" \
  --prompt "How many orders does this customer have?"

---

Project Structure

PyZen/
|
├── pyzen/
│   ├── __init__.py
│   ├── model.py
│   ├── runtime.py
│   ├── tools.py
│   └── cli.py
|
├── models/
│   ├── needle2.cact
│   └── README.txt
|
├── native/
│   └── README.txt
|
├── examples/
│   └── order_demo.py
|
├── tests/
│   └── test_tools.py
|
├── scripts/
│   └── install_termux.fish
|
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore

---

Runtime

The runtime is the bridge between PyZen and the underlying inference engine.

PyZen
  |
  v
model.py
  |
  v
runtime.py
  |
  v
Native Engine
  |
  v
Local AI

This architecture allows PyZen to replace the backend later without forcing application developers to rewrite their code.

---

Backend Architecture

The long-term backend architecture is:

                 PyZen API
                     |
               Runtime Layer
                     |
        +------------+------------+
        |            |            |
        v            v            v
     Android       Linux       Windows
      Engine       Engine       Engine
        |
        v
      macOS / WASM

The official Needle 2 distribution currently provides platform-specific native runners and libraries for Android, Linux, Windows, macOS and WebAssembly targets.

---

Linux Setup

Install the Python package:

python -m pip install cactus-needle

Download the Linux ARM64 engine:

needle download linux-arm64 --generation 2 --out ~/.pyzen/engine

For Linux x86-64:

needle download linux-x86_64 --generation 2 --out ~/.pyzen/engine

Then configure:

export PYZEN_ENGINE="$HOME/.pyzen/engine/linux-arm64/needle"

For x86-64:

export PYZEN_ENGINE="$HOME/.pyzen/engine/linux-x86_64/needle"

---

macOS Setup

Install:

python -m pip install cactus-needle

Apple Silicon:

needle download macos-arm64 --generation 2 --out ~/.pyzen/engine

Configure:

export PYZEN_ENGINE="$HOME/.pyzen/engine/macos-arm64/needle"

---

Windows Setup

Install:

python -m pip install cactus-needle

Download the Windows ARM64 engine:

needle download windows-arm64 --generation 2 --out "$HOME\.pyzen\engine"

For Windows x64:

needle download windows-x86_64 --generation 2 --out "$HOME\.pyzen\engine"

Set the engine:

$env:PYZEN_ENGINE="$HOME\.pyzen\engine\windows-arm64\needle.exe"

---

Running Tests

Install testing dependencies if necessary:

python -m pip install pytest

Run:

python -m pytest -q

Expected:

1 passed

---

Troubleshooting

Engine not found

If you see:

Native engine not found

Check:

echo $PYZEN_ENGINE

Then:

ls -lh "$PYZEN_ENGINE"

If necessary:

export PYZEN_ENGINE=/path/to/needle

---

Android Permission Error

Run:

chmod +x "$PYZEN_ENGINE"

Then:

"$PYZEN_ENGINE" --help

---

Model Checksum Failure

Run:

sha256sum models/needle2.cact

The expected current SHA256 is:

b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba

If it differs, download the model again.

---

Python Import Error

Run:

python -m pip install -e .

Then:

python -c "import pyzen; print(pyzen.__version__)"

---

Development

Clone the project:

git clone https://github.com/ZUYANX/PyZen.git
cd PyZen

Create a branch:

git checkout -b feature/my-feature

Install development version:

python -m pip install -e .

Run tests:

python -m pytest -q

---

Roadmap

PyZen 0.1

- [x] Python package
- [x] Runtime abstraction
- [x] Tool registry
- [x] Tool schema generation
- [x] Tool calling
- [x] Argument extraction
- [x] Python function execution
- [x] Android ARM64 testing
- [x] Termux testing
- [x] Basic test suite

PyZen 0.2

- [ ] Tool-result to final-answer loop
- [ ] Multiple tool calls
- [ ] Better error handling
- [ ] Conversation state
- [ ] Streaming
- [ ] Improved tool API
- [ ] More examples
- [ ] Better model management

PyZen 1.0

- [ ] Stable public API
- [ ] PyPI release
- [ ] Android backend
- [ ] Linux backend
- [ ] Windows backend
- [ ] macOS backend
- [ ] WASM backend
- [ ] Backend auto-detection
- [ ] Model management
- [ ] Production documentation
- [ ] Cross-platform release packages

---

Privacy

PyZen is designed around local inference.

The application can run its AI inference locally rather than sending prompts and tool data to a remote AI API.

Network access may still be required during initial installation or when downloading model/engine files.

Once the required files are available locally, the runtime can operate without requiring a remote AI API.

---

Performance

The current Android ARM64 development test achieved approximately:

Peak RAM:       ~24 MB
Prefill:        ~286 tok/s
Decode:         ~141 tok/s

These numbers are development measurements and should not be treated as universal benchmarks.

Performance depends on:

- Device CPU
- Architecture
- Thermal conditions
- Query length
- Tool schema size
- Output length
- Runtime version

---

Security

PyZen tools execute normal Python code.

Only register functions that your application is willing to expose to the AI runtime.

For example:

registry.register(check_orders)

is safe only if "check_orders" itself validates its inputs and permissions.

For production applications:

- Validate tool arguments.
- Authenticate sensitive operations.
- Apply authorization checks.
- Avoid exposing arbitrary shell execution.
- Avoid exposing unrestricted filesystem access.
- Log sensitive tool operations appropriately.
- Treat model-generated arguments as untrusted input.

---

Contributing

Contributions are welcome.

Before submitting a pull request:

1. Create a feature branch.
2. Keep changes focused.
3. Add tests for new functionality.
4. Run the test suite.
5. Update documentation when necessary.
6. Submit a pull request with a clear description.

Example:

git checkout -b feature/my-feature
python -m pytest -q
git add .
git commit -m "Add my feature"
git push origin feature/my-feature

---

License

PyZen is released under the MIT License.

See "LICENSE" (LICENSE) for details.

---

Acknowledgements

PyZen currently uses the Needle 2 native inference backend for its working implementation.

Needle 2 is an open on-device tool-calling model and provides platform-specific native runtimes and model artifacts.

PyZen provides the application-facing runtime, tool registry, and integration layer.

---

Author

MR ZUYAN

PyZen

Small AI. Big possibilities.

---

Vision

The long-term goal of PyZen is to provide a simple local AI interface:

from pyzen import PyZen

ai = PyZen("my-model")

result = ai(
    "Check the customer's latest order"
)

while PyZen handles the underlying runtime, model inference, tool selection, argument extraction, and application integration.

Build locally.
Run locally.
Integrate simply.
