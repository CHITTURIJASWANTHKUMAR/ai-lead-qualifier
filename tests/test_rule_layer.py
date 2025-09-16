import pytest
from scoring import role_relevance, industry_match, data_completeness, rule_score

def test_role_relevance():
    assert role_relevance("Head of Growth") == 20
    assert role_relevance("Marketing Manager") == 10
    assert role_relevance("Intern") == 0

def test_industry_match():
    icp = ["B2B SaaS mid-market"]
    assert industry_match("B2B SaaS mid-market", icp) == 20
    assert industry_match("SaaS", icp) == 10
    assert industry_match("Healthcare", icp) == 0

def test_data_completeness():
    lead = {"name": "Ava", "role": "Head", "company": "X", "industry": "Y", "location": "Z", "linkedin_bio": "bio"}
    assert data_completeness(lead) == 10
    lead_missing = {"name": "Ava", "role": "Head", "company": "X", "industry": "Y", "location": "Z"}
    assert data_completeness(lead_missing) == 0

def test_rule_score():
    offer = {"ideal_use_cases": ["B2B SaaS mid-market"]}
    lead = {"name": "Ava", "role": "Head of Growth", "company": "FlowMetrics", "industry": "B2B SaaS mid-market", "location": "NY", "linkedin_bio": "bio"}
    assert rule_score(lead, offer) == 50
