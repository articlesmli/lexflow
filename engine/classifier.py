from engine.parser import ManifestParser
from engine.classifier import EUAIActEngine

if __name__ == "__main__":
    try:
        # Load profile dynamically from the repo's manifest file
        profile = ManifestParser.parse_manifest("ai-manifest.yaml")
        
        engine = EUAIActEngine()
        result = engine.evaluate_system(profile)
        
        print(f"--- Audit Report for: {result.system_name} ---")
        print(f"Risk Tier: {result.risk_tier}")
        print(f"Triggered Frameworks: {result.triggered_articles}")
        print(f"Required Action: {result.action_required}")
        
    except Exception as e:
        print(f"❌ Compliance Audit Failed: {e}")
        exit(1)
