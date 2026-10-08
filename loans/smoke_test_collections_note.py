"""Drafts a collections note with an external language model."""
import openai


def collections_note(client):
    prompt = (
        f"Write a polite collections note for {client.first_name} {client.last_name}. "
        f"Email: {client.email}. Mobile: {client.mobile_number}. Annual income: {client.annual_income}."
    )
    reply = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return reply.choices[0].message.content
