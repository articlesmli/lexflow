#!/usr/bin/env bash
set -euo pipefail

MANIFEST_FILE="ai-manifest.yaml"
# Adjust this to point to your main entry point or validator script (e.g., engine/validator.py or main.py)
ENTRY_SCRIPT="main.py"

echo "=== Running LexFlow EU AI Act Compliance Linter ==="

if [ ! -f "$MANIFEST_FILE" ]; then
    echo "⚠️ Warning: No '$MANIFEST_FILE' found in this repository."
    exit 0
fi

if [ ! -f "$ENTRY_SCRIPT" ]; then
    echo "❌ Error: Entry point '$ENTRY_SCRIPT' not found."
    exit 1
fi

echo "🔍 Scanning manifest and evaluating against EU AI Act rules..."

# Run the Python script and capture its exit code and output
set +e
AUDIT_OUTPUT=$(python3 "$ENTRY_SCRIPT" 2>&1)
EXIT_CODE=$?
set -e

# Print the output so the ANSI color formatting displays cleanly in the terminal / GitHub Actions
echo "$AUDIT_OUTPUT"

# If the Python script already exited with a failure code (e.g., sys.exit(1) from validator.py), propagate it
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "\n\033[91m🚨 BUILD FAILED: LexFlow Compliance Gateway blocked the build.\033[0m"
    exit 1
fi

# Fallback string checks if the script didn't exit early
if echo "$AUDIT_OUTPUT" | grep -q "Risk Tier: Prohibited"; then
    echo -e "\n\033[91m🚨 BUILD FAILED: System categorized as 'Prohibited'.\033[0m"
    exit 1
else
    echo -e "\n\033[32m✅ Compliance check passed successfully.\033[0m"
    exit 0
fi