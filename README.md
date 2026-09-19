# LexFlow 🛡️🤖

> **Compliance-as-Code engine for automating EU AI Act regulatory auditing in CI/CD pipelines.**

LexFlow acts as an automated regulatory guardrail for software engineering teams. By validating your AI system manifests against an EU AI Act rulebook, LexFlow ensures that non-compliant or prohibited AI models (e.g., Article 5 violations) are automatically caught and blocked from merging into production.

---

## Architecture

LexFlow is built around three core components:
1. **The Rulebook (`rules/`):** A machine-readable Markdown document codifying articles, restrictions, and requirements of the EU AI Act (such as prohibited practices and high-risk classifications).
2. **The Compliance Engine (`engine/`):** A Python-based validation module that parses `ai-manifest.yaml` configurations and evaluates them against the rulebook.
3. **The CI/CD Gatekeeper (`.github/workflows/`):** A GitHub Actions workflow that executes `pytest` and a custom audit script on every Pull Request, failing the build and blocking merges if compliance violations are detected.

---

## Repository Structure

```text
lexflow/
├── .github/
│   └── workflows/
│       └── compliance.yml   # GitHub Actions CI gatekeeper workflow
├── engine/
│   └── validator.py         # Core Python validation and error formatting logic
├── rules/
│   └── eu_ai_act.md         # Markdown-based regulatory rulebook
├── tests/
│   └── test_engine.py       # Unit tests for compliance rules via pytest
├── audit.sh                 # Shell script runner for local/CI audits
└── ai-manifest.yaml         # Metadata configuration file for the AI system
