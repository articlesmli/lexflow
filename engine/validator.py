#!/usr/bin/env python3
import sys
import yaml
import os
import re

def search_codebase(file_path, pattern):
    """Searches a given source file for a specific code pattern or keyword."""
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
            return bool(re.search(pattern, source_code, re.IGNORECASE))
    except Exception:
        return False
# Global list to track violations found during the audit
violations_found = []

def report_violation(article_num, rule_name, reason, remediation):
    """Appends a violation to the tracking list and prints formatted error output."""
    violations_found.append(rule_name)
    # ANSI Color Codes for terminal formatting
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    print(f"{RED}{BOLD}🚨 Violation [{article_num} - {rule_name}]:{RESET}")
    print(f"   Reason: {reason}")
    print(f"   Remediation: {remediation}\n")

def check_article_5_prohibitions(manifest):
    """Evaluates AI system against EU AI Act Article 5 (Prohibited AI Practices)."""
    uses_biometrics = manifest.get("uses_biometrics", False)
    sector = manifest.get("sector", "").lower()
    
    # Example rule: Real-time biometric identification in law enforcement is prohibited
    if uses_biometrics and sector == "law enforcement":
        report_violation(
            article_num="Article 5",
            rule_name="Prohibited Biometric Practice",
            reason="Real-time remote biometric identification in publicly accessible spaces for law enforcement is strictly prohibited.",
            remediation="Disable biometric processing or modify the deployment sector."
        )

def check_article_10_data_governance(manifest):
    """Evaluates High-Risk AI systems against Article 10 by verifying both manifest and code-level data governance frameworks."""
    risk_tier = manifest.get("risk_tier", "").lower()
    has_policy_manifest = manifest.get("has_data_governance_policy", False)
    
    # Scan source code for data governance hooks, lineage logging, or tracking frameworks (e.g., MLflow, Wandb, or bias audits)
    code_has_governance_hooks = search_codebase(
        "main.py", 
        r"def\s+.*audit_bias.*|import\s+mlflow|import\s+wandb|log_dataset_lineage|track_dataset"
    )
    
    if risk_tier == "high-risk":
        if not has_policy_manifest:
            report_violation(
                article_num="Article 10",
                rule_name="Data Governance (Manifest Missing)",
                reason="High-risk AI systems must declare a data governance policy in the manifest.",
                remediation="Set 'has_data_governance_policy: true' once data governance frameworks are integrated."
            )
        elif not code_has_governance_hooks:
            report_violation(
                article_num="Article 10",
                rule_name="Data Governance (Code Mismatch)",
                reason="Manifest claims data governance, but no bias auditing functions, dataset lineage logging, or ML tracking frameworks were found in 'main.py'.",
                remediation="Integrate a data tracking tool or implement a `log_dataset_lineage` / `audit_bias` function in your source code."
            )

def check_article_14_human_oversight(manifest):
    """Evaluates High-Risk AI systems against Article 14 by verifying both manifest and source code."""
    risk_tier = manifest.get("risk_tier", "").lower()
    has_oversight_manifest = manifest.get("has_human_oversight", False)
    
    # Define what a real human oversight implementation looks like in code
    # e.g., looking for a function named 'human_review' or a decorator like '@requires_approval'
    code_has_oversight_hook = search_codebase("main.py", r"def\s+.*human_review.*|@requires_approval")
    
    if risk_tier == "high-risk":
        if not has_oversight_manifest:
            report_violation(
                article_num="Article 14",
                rule_name="Human Oversight (Manifest Missing)",
                reason="High-risk AI systems must declare human oversight in the manifest.",
                remediation="Set 'has_human_oversight: true' once implementation is complete."
            )
        elif not code_has_oversight_hook:
            report_violation(
                article_num="Article 14",
                rule_name="Human Oversight (Code Mismatch)",
                reason="Manifest claims human oversight, but no review functions or approval decorators were found in 'main.py'.",
                remediation="Implement a human-in-the-loop review function or decorator in your source code."
            )

def check_article_52_transparency(manifest):
    """Evaluates AI systems against Article 52 Transparency and Synthetic Content Disclosure requirements."""
    generates_synthetic = manifest.get("generates_synthetic_content", False)
    is_customer_facing = manifest.get("is_customer_facing", False)
    has_disclosure = manifest.get("has_synthetic_content_disclosure", False)
    
    if (generates_synthetic or is_customer_facing) and not has_disclosure:
        report_violation(
            article_num="Article 52",
            rule_name="Transparency & Synthetic Content Disclosure",
            reason="AI systems generating synthetic content or interacting directly with natural persons must disclose that the user is interacting with an AI or that content is artificially generated.",
            remediation="Set 'has_synthetic_content_disclosure: true' and ensure machine-readable marking or user notices are implemented."
        )

def validate_manifest():
    """Main orchestrator to load the manifest and execute all regulatory rule checks."""
    manifest_path = "ai-manifest.yaml"
    
    print("=== Running LexFlow EU AI Act Compliance Linter ===")
    print("🔍 Scanning manifest and evaluating against EU AI Act rules...")
    
    try:
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"⚠️ Warning: No '{manifest_path}' found in repository root.")
        sys.exit(1)
        
    system_name = manifest.get("system_name", "Unnamed AI System")
    risk_tier = manifest.get("risk_tier", "Unknown")
    
    print(f"=== Audit Report: {system_name} ===")
    print(f"Risk Tier: {risk_tier}\n")
    
    # Execute rule checks
    check_article_5_prohibitions(manifest)
    check_article_10_data_governance(manifest)
    check_article_14_human_oversight(manifest)
    check_article_52_transparency(manifest)
    
    # Final gatekeeper decision based on tracked violations
    if len(violations_found) > 0:
        print(f"❌ Compliance check failed with {len(violations_found)} violation(s).")
        sys.exit(1)
    else:
        print("✅ Compliance check passed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    validate_manifest()