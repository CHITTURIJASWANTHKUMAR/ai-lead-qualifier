# Rule-based scoring logic for lead intent

ROLE_DECISION_MAKERS = ["Head", "Director", "VP", "Chief", "Founder", "Owner"]
ROLE_INFLUENCERS = ["Manager", "Lead", "Specialist"]

def role_relevance(role: str) -> int:
    if any(title in role for title in ROLE_DECISION_MAKERS):
        return 20
    if any(title in role for title in ROLE_INFLUENCERS):
        return 10
    return 0

def industry_match(lead_industry: str, icp_list: list) -> int:
    if not icp_list:
        return 0
    for icp in icp_list:
        if lead_industry.lower() == icp.lower():
            return 20
        if lead_industry.lower() in icp.lower() or icp.lower() in lead_industry.lower():
            return 10
    return 0

def data_completeness(lead: dict) -> int:
    required_fields = ["name", "role", "company", "industry", "location", "linkedin_bio"]
    if all(lead.get(f) for f in required_fields):
        return 10
    return 0

def rule_score(lead: dict, offer: dict) -> int:
    score = 0
    score += role_relevance(lead.get("role", ""))
    score += industry_match(lead.get("industry", ""), offer.get("ideal_use_cases", []))
    score += data_completeness(lead)
    return score
