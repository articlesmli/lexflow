# EU AI Act Master Rulebook

## Prohibited Practices (Article 5)
- **Condition:** uses_biometrics == true and sector == "Law Enforcement" and target_audience == "children"
- **Risk Tier:** Prohibited
- **Articles:** Article 5
- **Action:** IMMEDIATE HALT: System design violates core EU prohibitions.

## High-Risk Categories (Annex III)
- **Condition:** sector in ["HR", "Employment", "Recruitment", "Critical Infrastructure"]
- **Risk Tier:** High-Risk
- **Articles:** Annex III (Employment & Infrastructure)
- **Action:** Full Annex IV Technical Documentation required.

## Transparency Obligations (Article 50)
- **Condition:** generates_synthetic_content == true or is_customer_facing == true
- **Risk Tier:** Transparency / Limited Risk
- **Articles:** Article 50 (Transparency Obligations)
- **Action:** Ensure users are explicitly informed they are interacting with an AI.