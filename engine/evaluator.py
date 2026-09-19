from engine.rule_loader import MarkdownRuleLoader
from engine.parser import AISystemProfile

class ComplianceEvaluator:
    """
    Dynamically evaluates an AI system profile against rules defined in the markdown rulebook.
    """
    def __init__(self, rule_path: str = "rules/eu_ai_act_rules.md"):
        self.rules = MarkdownRuleLoader.load_rules(rule_path)

    def evaluate(self, profile: AISystemProfile) -> dict:
        # Map profile attributes into a safe local context dictionary
        context = {
            "sector": profile.sector,
            "uses_biometrics": profile.uses_biometrics,
            "is_customer_facing": profile.is_customer_facing,
            "generates_synthetic_content": profile.generates_synthetic_content,
            "target_audience": profile.target_audience,
        }

        matched_violations = []
        highest_risk = "Minimal / Low Risk"
        triggered_articles = []
        required_action = "No mandatory legal barriers. Voluntary codes of conduct recommended."

        # Risk level ranking to prioritize severe classifications
        risk_hierarchy = {
            "Minimal / Low Risk": 0,
            "Transparency / Limited Risk": 1,
            "High-Risk": 2,
            "Prohibited": 3
        }

        for rule in self.rules:
            raw_condition = rule.get("condition")
            if not raw_condition:
                continue
            
            # Normalize condition text: ensure Python-compatible True/False capitalization
            condition = (
                raw_condition.replace("true", "True")
                             .replace("false", "False")
            )
            
            # Safely evaluate the condition string using a restricted namespace
            try:
                is_triggered = eval(condition, {"__builtins__": None}, context)
            except Exception as e:
                print(f"⚠️ Error evaluating rule condition '{raw_condition}': {e}")
                continue

            if is_triggered:
                risk_tier = rule.get("risk_tier", "Minimal / Low Risk")
                article = rule.get("articles", "General provisions")
                if article:
                    triggered_articles.append(article)
                
                # Escalate risk tier if current rule is more critical
                if risk_hierarchy.get(risk_tier, 0) > risk_hierarchy.get(highest_risk, 0):
                    highest_risk = risk_tier
                    required_action = rule.get("action", required_action)
                
                if risk_tier in ["Prohibited", "High-Risk"]:
                    matched_violations.append(f"[{rule.get('title', 'Rule')}] {rule.get('action', '')}")

        return {
            "system_name": profile.name,
            "risk_tier": highest_risk,
            "triggered_articles": list(set(triggered_articles)),
            "action_required": required_action,
            "violations": matched_violations
        }