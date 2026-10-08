"""Writes a payment reminder with an external language model."""
import openai


def reminder_text(client):
    prompt = (
        f"Write a friendly payment reminder for {client.first_name}. "
        f"Tax id: {client.tax_id}. Phone number: {client.phone_number}."
    )
    reply = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return reply.choices[0].message.content
