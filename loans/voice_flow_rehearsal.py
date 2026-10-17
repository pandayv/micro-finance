"""Drafts a goodwill message with an external language model."""
import openai


def goodwill_message(client):
    prompt = (
        f"Write a goodwill message for {client.first_name} {client.last_name}. "
        f"Email: {client.email}. Phone number: {client.phone_number}. Tax id: {client.tax_id}."
    )
    reply = openai.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return reply.choices[0].message.content
