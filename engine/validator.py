#!/usr/bin/env python3
import sys
import yaml

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
    """Evaluates High-Risk AI systems against Article 10 Data Governance requirements."""
    risk_tier = manifest.get("risk_tier", "").lower()
    has_policy = manifest.get("has_data_governance_policy", False)
    
    if risk_tier == "high-risk" and not has_policy:
        report_violation(
            article_num="Article 10",
            rule_name="Data Governance",
            reason="High-risk AI systems must implement data governance and bias monitoring frameworks.",
            remediation="Set 'has_data_governance_policy: true' and link your governance documentation in the manifest."
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
    
    # Final gatekeeper decision based on tracked violations
    if len(violations_found) > 0:
        print(f"❌ Compliance check failed with {len(violations_found)} violation(s).")
        sys.exit(1)
    else:
        print("✅ Compliance check passed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    validate_manifest()