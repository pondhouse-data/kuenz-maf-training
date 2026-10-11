"""Schritt 2: Der Agent bekommt Tools und antwortet aus unseren Daten.

Starten: Run and Debug → Debug Local Agent HTTP Server → F5 → 02-tools.
Im Agent Inspector fragen: „Was gilt für R-03 bei A-100?“
"""
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from tools import aktuelle_uhrzeit, lade_anforderungskatalog, lade_pruefauftrag, lade_spezifikation


def erstelle_agent():
    load_dotenv()
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )
    return Agent(
        client=client,
        name="PruefAgent",
        instructions=(
            "Du hilfst bei der Prüfung von Kundenspezifikationen. "
            "Beantworte Fragen zu Prüfaufträgen, Anforderungen und Spezifikationen nur mit den Tools. "
            "Liefert ein Tool einen Fehler, sag das und erfinde nichts. Antworte kurz und auf Deutsch."
        ),
        tools=[aktuelle_uhrzeit, lade_pruefauftrag, lade_anforderungskatalog, lade_spezifikation],
        default_options={"store": False},
    )


if __name__ == "__main__":
    ResponsesHostServer(erstelle_agent).run()
