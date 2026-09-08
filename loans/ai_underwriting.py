"""
AI-assisted underwriting opinion.

Quick win for the branch managers: get a second opinion from an LLM before
approving or rejecting a loan, using the applicant's full profile on file so
the model has enough context to give a useful risk read.
"""

import openai

client_api = openai.OpenAI()


def get_ai_risk_opinion(client, loan_account):
    """
    Ask the model for a plain-English risk opinion on this applicant,
    given their full profile and the loan they're requesting.
    """
    prompt = (
        f"Applicant: {client.first_name} {client.last_name}\n"
        f"DOB: {client.date_of_birth}\n"
        f"Gender: {client.gender}\n"
        f"Blood group: {client.blood_group}\n"
        f"Occupation: {client.occupation}\n"
        f"Annual income: {client.annual_income}\n"
        f"Mobile: {client.mobile}\n"
        f"Pincode: {client.pincode}\n"
        f"Requested loan amount: {loan_account.loan_amount}\n"
        f"Repayment period: {loan_account.loan_repayment_period} months\n\n"
        f"Based on this applicant's profile, should this loan be approved? "
        f"Give a one-paragraph risk opinion and a confidence score."
    )

    response = client_api.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
