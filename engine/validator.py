import sys

def report_violation(article_num: str, rule_name: str, reason: str, remediation: str):
    """Prints a beautifully formatted compliance failure banner and exits."""
    # ANSI color codes for terminal formatting
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    print(f"\n{RED}{BOLD}[LEXFLOW COMPLIANCE GATEWAY: FAILED]{RESET}")
    print(f"{RED}──────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}Rule Violated:{RESET} {article_num} - {rule_name}")
    print(f"{BOLD}Reason:{RESET}        {YELLOW}{reason}{RESET}")
    print(f"{BOLD}Action Required:{RESET} {remediation}")
    print(f"{RED}──────────────────────────────────────────────────{RESET}\n")
    
    # Exit with a non-zero status to fail the CI/CD pipeline
    sys.exit(1)

def validate_manifest(manifest_data):
    """Validates the ai-manifest against EU AI Act regulations."""
    
    # Check for Article 5 Prohibited AI Practices
    is_law_enforcement = manifest_data.get("sector", "").lower() == "law enforcement"
    uses_biometrics = manifest_data.get("uses_biometrics", False)
    
    if is_law_enforcement and uses_biometrics:
        report_violation(
            article_num="Article 5",
            rule_name="Prohibited AI Practices",
            reason="Unreal-time/remote biometric identification or categorization in law enforcement is strictly banned.",
            remediation="Remove biometric tracking features or adjust the deployment sector."
        )
    
    print("\033[92m[LEXFLOW] AI Manifest passed all EU AI Act compliance checks.\033[0m")import sys

def report_violation(article_num: str, rule_name: str, reason: str, remediation: str):
    """Prints a beautifully formatted compliance failure banner and exits."""
    # ANSI color codes for terminal formatting
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    print(f"\n{RED}{BOLD}[LEXFLOW COMPLIANCE GATEWAY: FAILED]{RESET}")
    print(f"{RED}──────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}Rule Violated:{RESET} {article_num} - {rule_name}")
    print(f"{BOLD}Reason:{RESET}        {YELLOW}{reason}{RESET}")
    print(f"{BOLD}Action Required:{RESET} {remediation}")
    print(f"{RED}──────────────────────────────────────────────────{RESET}\n")
    
    # Exit with a non-zero status to fail the CI/CD pipeline
    sys.exit(1)

def validate_manifest(manifest_data):
    """Validates the ai-manifest against EU AI Act regulations."""
    
    # Check for Article 5 Prohibited AI Practices
    is_law_enforcement = manifest_data.get("sector", "").lower() == "law enforcement"
    uses_biometrics = manifest_data.get("uses_biometrics", False)
    
    if is_law_enforcement and uses_biometrics:
        report_violation(
            article_num="Article 5",
            rule_name="Prohibited AI Practices",
            reason="Unreal-time/remote biometric identification or categorization in law enforcement is strictly banned.",
            remediation="Remove biometric tracking features or adjust the deployment sector."
        )
    
    print("\033[92m[LEXFLOW] AI Manifest passed all EU AI Act compliance checks.\033[0m")
