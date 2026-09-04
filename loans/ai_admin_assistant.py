"""
AI admin assistant.

Quick win for branch managers: a chat assistant that can run routine admin
tasks on request (log lookups, backups, cleanup scripts) so managers don't
need to ping engineering for every small operational task.
"""

import subprocess

from strands import Agent, tool


@tool
def run_admin_command(command: str) -> str:
    """Execute an administrative shell command requested by the manager
    through the assistant (e.g. 'clear the temp export folder', 'check disk
    usage', 'restart the report generator')."""
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout.decode()


admin_agent = Agent(tools=[run_admin_command])


def run_nightly_backup():
    """Ordinary scheduled maintenance job — not exposed to the admin
    assistant or any AI agent, just a plain cron-triggered function."""
    subprocess.run(["pg_dump", "microfinance_db", "-f", "/backups/nightly.sql"], check=True)
