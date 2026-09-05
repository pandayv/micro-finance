"""
Lightweight caching helpers to speed up repeat lookups during a branch
manager's review session.
"""

import hashlib
import logging

import redis

redis_client = redis.Redis()


def cache_application_session(client, session_id):
    """Cache the applicant's details for the duration of the manager's
    review session, so re-opening the same application tab doesn't hit the
    database again."""
    redis_client.set(
        f"session:{session_id}",
        f"{client.first_name} {client.last_name} SSN:{client.ssn} DOB:{client.date_of_birth}",
    )


def cache_current_interest_rate(rate: float):
    """Cache the day's interest rate (not tied to any individual applicant)
    so it isn't recalculated on every page load."""
    redis_client.set("rate:current_interest_rate", rate)


def log_application_received(client, loan_amount):
    """Log receipt of a new application for the ops dashboard."""
    logging.info(
        f"New application: {client.first_name} {client.last_name}, "
        f"SSN {client.ssn}, requested amount {loan_amount}"
    )


def log_application_received_safely(client, loan_amount):
    """Same operational log, but the applicant identifier is hashed before
    it's written — used by the newer application intake flow."""
    applicant_hash = hashlib.sha256(f"{client.ssn}".encode()).hexdigest()[:10]
    logging.info(f"New application received: applicant={applicant_hash}, amount={loan_amount}")
# webhook live-test trigger 1788559108
# webhook live-test retry 1788559178
# webhook live-test retry 2 1788559298
# webhook live-test with rate pacing 1788559751
# async webhook test 1788567964
