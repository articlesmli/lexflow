import pytest
from engine.parser import AISystemProfile
from engine.evaluator import ComplianceEvaluator

@pytest.fixture
def evaluator():
    # Points to your active markdown rulebook
    return ComplianceEvaluator("rules/eu_ai_act_rules.md")

def test_prohibited_system(evaluator):
    # Scenario: Law enforcement biometric targeting of children (Article 5)
    profile = AISystemProfile(
        name="IllegalBiometricTracker",
        sector="Law Enforcement",
        uses_biometrics=True,
        is_customer_facing=False,
        generates_synthetic_content=False,
        target_audience="children"
    )
    result = evaluator.evaluate(profile)
    assert result["risk_tier"] == "Prohibited"
    assert "Article 5" in result["triggered_articles"]

def test_high_risk_system(evaluator):
    # Scenario: AI resume screener in the HR sector (Annex III)
    profile = AISystemProfile(
        name="HRResumeScreener",
        sector="HR",
        uses_biometrics=False,
        is_customer_facing=False,
        generates_synthetic_content=False,
        target_audience="workers"
    )
    result = evaluator.evaluate(profile)
    assert result["risk_tier"] == "High-Risk"
    assert any("Annex III" in article for article in result["triggered_articles"])

def test_transparency_system(evaluator):
    # Scenario: Customer-facing retail chatbot (Article 50)
    profile = AISystemProfile(
        name="RetailChatbot",
        sector="Retail",
        uses_biometrics=False,
        is_customer_facing=True,
        generates_synthetic_content=True,
        target_audience="general public"
    )
    result = evaluator.evaluate(profile)
    assert result["risk_tier"] == "Transparency / Limited Risk"
    assert "Article 50 (Transparency Obligations)" in result["triggered_articles"]

def test_minimal_risk_system(evaluator):
    # Scenario: Internal inventory database indexer
    profile = AISystemProfile(
        name="InventoryIndexer",
        sector="Logistics",
        uses_biometrics=False,
        is_customer_facing=False,
        generates_synthetic_content=False,
        target_audience="internal staff"
    )
    result = evaluator.evaluate(profile)
    assert result["risk_tier"] == "Minimal / Low Risk"
