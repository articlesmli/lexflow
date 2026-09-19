import os
import re
from typing import List, Dict, Any

class MarkdownRuleLoader:
    @staticmethod
    def load_rules(file_path: str = "rules/eu_ai_act_rules.md") -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing legal rulebook: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        rules = []
        sections = content.split("## ")
        
        for section in sections[1:]:
            lines = section.strip().split("\n")
            rule_title = lines[0].strip()
            
            rule_data = {"title": rule_title, "condition": "", "risk_tier": "", "articles": "", "action": ""}
            
            for line in lines[1:]:
                # Use regex to isolate the exact value after the label, stripping all leading markdown/symbols
                if "Condition:" in line:
                    val = re.sub(r'^[\s\-*`#]+', '', line.split("Condition:", 1)[1])
                    rule_data["condition"] = val.replace("**", "").strip()
                elif "Risk Tier:" in line:
                    val = re.sub(r'^[\s\-*`#]+', '', line.split("Risk Tier:", 1)[1])
                    rule_data["risk_tier"] = val.replace("**", "").strip()
                elif "Articles:" in line:
                    val = re.sub(r'^[\s\-*`#]+', '', line.split("Articles:", 1)[1])
                    rule_data["articles"] = val.replace("**", "").strip()
                elif "Action:" in line:
                    val = re.sub(r'^[\s\-*`#]+', '', line.split("Action:", 1)[1])
                    rule_data["action"] = val.replace("**", "").strip()
            
            if rule_data["condition"]:
                rules.append(rule_data)
                
        return rules