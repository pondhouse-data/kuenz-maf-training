"""Schritt 4: Der Prüfagent bekommt die Extraktion als Tool.

Starten: Run and Debug → Debug Local Agent HTTP Server → F5 → 04-extraktion.
Im Agent Inspector fragen: „Welche Angaben macht Version 2 der Spezifikation zu R-04?“
"""
import os
import time

from agent_framework import Agent, FunctionInvocationContext, function_middleware
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from extraktion import extrahiere_angaben
from tools import aktuelle_uhrzeit, lade_anforderungskatalog, lade_pruefauftrag, lade_spezifikation


@function_middleware
async def zeige_toolaufruf(context: FunctionInvocationContext, call_next) -> None:
    start = time.perf_counter()
    await call_next()
    print(f"  [Tool {context.function.name}, {time.perf_counter() - start:.2f} s]", flush=True)


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
        tools=[aktuelle_uhrzeit, lade_pruefauftrag, lade_anforderungskatalog, lade_spezifikation, extrahiere_angaben],
        middleware=[zeige_toolaufruf],
        default_options={"store": False},
    )


if __name__ == "__main__":
    ResponsesHostServer(erstelle_agent).run()
