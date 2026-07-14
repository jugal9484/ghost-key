#!/usr/bin/env bash
# Ghost Key launcher for Linux/macOS
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
    exec python3 -m password_toolkit "$@"
else
    exec python -m password_toolkit "$@"
fi
