# LexFlow 

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

LexFlow/
│
├── .github/
│   └── workflows/
│       └── compliance.yml          # GitHub Action: Triggers audit.sh on push/PR
│
├── engine/
│   ├── __init__.py
│   ├── classifier.py               # Reads and validates 'ai-manifest.yaml' files
│   ├── parser.py                   # Reads and validates 'ai-manifest.yaml' files
│   ├── rule_loader.py              # Parses partner's markdown rules
│   └── evaluator.py                # Core logic matching profile to rules
│
├── rules/
│   └── eu_ai_act_rules.md          # Dynamic legal rulebook maintained by your partner
│
├── tests/
│   └── test_compliance.py          # Automated test suite
│
├── main.py                         # Main entry point (runs the full pipeline)
├── audit.sh                        # Bash script (CI/CD gatekeeper / compliance linter)
├── Dockerfile                      # Containerizes the tool for secure, portable execution
├── ai-manifest.yaml                # Developer configuration template inside target repos
└── README.md                       # Project documentation for developers & legal teams
