from engine.parser import ManifestParser
from engine.evaluator import ComplianceEvaluator

if __name__ == "__main__":
    try:
        # 1. Parse developer manifest from the repo
        profile = ManifestParser.parse_manifest("ai-manifest.yaml")
        
        # 2. Run the dynamic markdown-backed compliance engine
        evaluator = ComplianceEvaluator("rules/eu_ai_act_rules.md")
        result = evaluator.evaluate(profile)
        
        # 3. Print out the audit report for CI/CD logging
        print(f"=== Audit Report: {result['system_name']} ===")
        print(f"Risk Tier: {result['risk_tier']}")
        print(f"Triggered Articles: {result['triggered_articles']}")
        print(f"Required Action: {result['action_required']}")
        
        if result['violations']:
            print("\n🚨 Violations Found:")
            for v in result['violations']:
                print(f" - {v}")
                
    except Exception as e:
        print(f"❌ Compliance Audit Crashed: {e}")
        exit(1)
