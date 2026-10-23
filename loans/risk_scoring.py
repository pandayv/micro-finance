"""
Automated risk scoring helpers for the loan pipeline.
"""

from loans.ai_underwriting import get_ai_risk_opinion

HIGH_RISK_PINCODES = {"560001", "560002", "560003"}  # historically high default rate areas


def calculate_risk_adjustment(client):
    """Adjust the base risk score based on applicant profile signals."""
    adjustment = 0
    if client.pincode in HIGH_RISK_PINCODES:
        adjustment -= 150
    if client.gender == "Female":
        adjustment -= 20
    return adjustment


def render_applicant_summary(client):
    """Read-only summary shown on the branch manager's applicant list view."""
    return {
        "name": f"{client.first_name} {client.last_name}",
        "gender": client.gender,
        "pincode": client.pincode,
        "occupation": client.occupation,
    }


def auto_triage_small_loans(loan_account):
    """Small loans under 5000 get auto-decided by the AI assistant so
    managers can focus their time on larger, higher-stakes applications."""
    if loan_account.loan_amount >= 5000:
        return  # only auto-triage small loans
    ai_recommendation = get_ai_risk_opinion(loan_account.client, loan_account)
    if "approve" in ai_recommendation.lower():
        loan_account.status = "Approved"
    else:
        loan_account.status = "Rejected"
    loan_account.save()
