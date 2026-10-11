"""Hosting-Einstieg: eine frische Workflow-Instanz je Anfrage.

Lokal: Run and Debug → Debug Local Agent HTTP Server → F5 → 07-hosting.
Deployment: 07-hosting in VS Code öffnen, dann Code → Remote.
"""
from agent_framework_foundry_hosting import ResponsesHostServer
from dotenv import load_dotenv

from workflow import erstelle_agent


if __name__ == "__main__":
    load_dotenv()
    ResponsesHostServer(erstelle_agent, history_source="agent").run()
