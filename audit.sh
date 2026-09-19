#!/usr/bin/env bash
set -euo pipefail

MANIFEST_FILE="ai-manifest.yaml"
MAIN_SCRIPT="main.py"

echo "=== Running EU AI Act Compliance Linter ==="

if [ ! -f "$MANIFEST_FILE" ]; then
    echo "⚠️ Warning: No '$MANIFEST_FILE' found in this repository."
    exit 0
fi

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "❌ Error: Entry point '$MAIN_SCRIPT' not found."
    exit 1
fi

echo "🔍 Scanning manifest and evaluating against EU AI Act rules..."

# Run the Python orchestrator
AUDIT_OUTPUT=$(python3 "$MAIN_SCRIPT")
echo "$AUDIT_OUTPUT"

# Check the output for violations
if echo "$AUDIT_OUTPUT" | grep -q "Risk Tier: Prohibited"; then
    echo "🚨 BUILD FAILED: System categorized as 'Prohibited'."
    exit 1
elif echo "$AUDIT_OUTPUT" | grep -q "Risk Tier: High-Risk"; then
    echo "⚠️ BUILD WARNING: System categorized as 'High-Risk'."
    exit 0
else
    echo "✅ Compliance check passed successfully."
    exit 0
fi