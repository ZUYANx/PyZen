#!/usr/bin/env fish
# Run from the project root in Termux.
set -l PREFIX (string trim -r --chars=/ $PREFIX)
mkdir -p ~/pyzen-test
cp ~/pyzen-test/needle2.cact models/needle2.cact 2>/dev/null
echo "Set PYZEN_ENGINE to an Android-compatible shared library before using ctypes runtime."
