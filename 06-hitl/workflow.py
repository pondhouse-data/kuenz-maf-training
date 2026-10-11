"""Schritt 5: Die Prüfung als Workflow aus vier festen Schritten, als Agent für den Responses-Server.

Starten: Run and Debug → Debug Local Agent HTTP Server → F5 → 05-workflow.
Im Agent Inspector senden: „Prüfe PR-001“
"""

import json
import os
import re
from typing import Never
from uuid import uuid4

from agent_framework import Agent, Executor, Message, WorkflowBuilder, WorkflowContext, handler
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from extraktion import ANWEISUNG, extrahiere
from regeln import bewerte
from tools import lade_anforderungskatalog, lade_pruefauftrag, lade_spezifikation


class AuftragLaden(Executor):
    @handler
    async def laden(self, nachrichten: list[Message], ctx: WorkflowContext[dict, str]) -> None:
        treffer = re.search(r"PR-\d{3}", nachrichten[-1].text.upper())
        auftrag = lade_pruefauftrag(treffer.group(0) if treffer else "")
        if "fehler" in auftrag:
            await ctx.yield_output(json.dumps(auftrag, ensure_ascii=False))
            return
        await ctx.send_message({"auftrag": auftrag})


class AngabenExtrahieren(Executor):
    def __init__(self, agent: Agent):
        super().__init__(id="angaben_extrahieren")
        self.agent = agent

    @handler
    async def extrahieren(self, daten: dict, ctx: WorkflowContext[dict]) -> None:
        extraktion = await extrahiere(self.agent, daten["auftrag"]["document_version"])
        await ctx.send_message({**daten, "angaben": extraktion.model_dump()["angaben"]})


class Vergleichen(Executor):
    @handler
    async def vergleichen(self, daten: dict, ctx: WorkflowContext[dict]) -> None:
        auftrag = daten["auftrag"]
        katalog = lade_anforderungskatalog(auftrag["asset_id"])
        spezifikation = lade_spezifikation(auftrag["document_version"])
        angaben = {a["requirement_id"]: a for a in daten["angaben"]}
        leer = {"fundstellen": [], "bewertung_vorschlag": None}
        befunde = [bewerte(a, angaben.get(a["requirement_id"], leer), spezifikation) for a in katalog["requirements"]]
        await ctx.send_message({**daten, "befunde": befunde})


class ErgebnisAusgeben(Executor):
    @handler
    async def ausgeben(self, daten: dict, ctx: WorkflowContext[Never, str]) -> None:
        auftrag = daten["auftrag"]
        await ctx.yield_output(json.dumps({
            "review_id": auftrag["review_id"],
            "run_id": str(uuid4()),
            "asset_id": auftrag["asset_id"],
            "document_id": auftrag["document_id"],
            "document_version": auftrag["document_version"],
            "befunde": daten["befunde"],
            "klaerungspunkte": [b for b in daten["befunde"] if b["status"] != "erfüllt"],
        }, ensure_ascii=False))


def baue_workflow(agent: Agent):
    schritte = [AuftragLaden(id="auftrag_laden"), AngabenExtrahieren(agent),
                Vergleichen(id="vergleichen"), ErgebnisAusgeben(id="ergebnis_ausgeben")]
    return WorkflowBuilder(name="spezifikationspruefung", start_executor=schritte[0]).add_chain(schritte).build()


def erstelle_workflow():
    """Baut einen frischen Prüfworkflow mit eigenem Extraktionsagenten."""
    load_dotenv()
    client = FoundryChatClient(project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                               model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"], credential=DefaultAzureCredential())
    return baue_workflow(Agent(client=client, name="Extraktion", instructions=ANWEISUNG))


def erstelle_agent():
    """Der ganze Workflow als ein Agent: Eingabe „Prüfe PR-001“, Ausgabe das Ergebnis als JSON."""
    return erstelle_workflow().as_agent(name="Spezifikationspruefung")
