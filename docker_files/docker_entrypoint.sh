#!/usr/bin/env bash

if [ -z "$ROOT_DIR" ]; then
    echo "ROOT_DIR is not set. Exiting."
    exit 1
fi

if [ -z "$MODE" ]; then
    MODE="release"
fi

source venv/bin/activate
echo "Working directory: $(pwd)"
echo "Running in mode $MODE."

if [ "$MODE" = "release" ]; then
    python3 -m "$ROOT_DIR" "$@"
fi
if [ "$MODE" = "it" ]; then
    bash
fi
echo "Completed in mode $MODE."
