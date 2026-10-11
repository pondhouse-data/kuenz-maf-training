"""Schritt 4: Das Modell liest die Spezifikation und liefert Angaben in einem festen Schema.

Der Prüfagent in main.py ruft die Extraktion als Tool extrahiere_angaben auf.
"""

import os
from typing import Annotated, Literal

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel, Field

from tools import lade_anforderungskatalog, lade_spezifikation


class Fundstelle(BaseModel):
    abschnitt: str = Field(description="Abschnittsnummer ohne §, z. B. 3.2 oder A.1")
    zitat: str = Field(description="Wörtlicher Ausschnitt aus genau diesem Abschnitt, 3 bis 12 Wörter")
    werte: list[str] = Field(description="Werte aus dem Zitat im Format, das die Anweisung je Anforderung vorgibt")


class Angabe(BaseModel):
    requirement_id: str = Field(description="R-01 bis R-06")
    fundstellen: list[Fundstelle] = Field(description="Leer, wenn die Spezifikation dazu nichts sagt")
    bewertung_vorschlag: Literal["erfüllt", "abweichend", "unklar"] | None = Field(description="Nur für R-06, sonst null")
    begruendung: str = Field(description="Ein Satz: was steht wo, oder warum nichts gefunden wurde")


class Extraktion(BaseModel):
    angaben: list[Angabe]


ANWEISUNG = """Du liest eine Kundenspezifikation und suchst Angaben zu den Anforderungen R-01 bis R-06.
Du entscheidest NICHT, ob eine Anforderung erfüllt ist; das macht danach der Code. Ausnahme: R-06.

- Verwende nur den gelieferten Text, kein Vorwissen. Lies das ganze Dokument bis zum Ende, auch den Anhang (Abschnitte A.x).
- Liefere für jede Anforderung R-01 bis R-06 genau einen Eintrag.
- Eine Fundstelle besteht aus Abschnittsnummer und einem wörtlichen Zitat, genau wie im Text.
- Nimm nur Angaben, die genau den Gegenstand der Anforderung betreffen.
- Nennt das Dokument an mehreren Stellen unterschiedliche Werte, liefere ALLE diese Fundstellen.
- Findest du nichts, bleibt fundstellen leer. Erfinde nichts.
- Format der werte: R-01 Sprachcodes wie ["DE", "EN"] · R-02 Zahl in t wie ["41"] · R-03 Versionsnummer wie ["1.4"]
  · R-04 Zahl in ms wie ["30"] · R-05 Minimum und Maximum in °C wie ["-20", "40"] · R-06 [] und dazu bewertung_vorschlag.
"""


def baue_prompt(document_version: str) -> str:
    katalog = lade_anforderungskatalog("A-100")
    spezifikation = lade_spezifikation(document_version)
    anforderungen = "\n".join(f"{a['requirement_id']} {a['thema']}: {a['soll']}" for a in katalog["requirements"])
    text = "\n".join(f"§{a['abschnitt']} {a['titel']}: {a['text']}" for a in spezifikation["abschnitte"])
    return f"Anforderungen:\n{anforderungen}\n\nSpezifikation SPEC-001 Version {document_version}:\n{text}"


async def extrahiere(agent: Agent, document_version: str) -> Extraktion:
    response = await agent.run(baue_prompt(document_version), options={"response_format": Extraktion, "reasoning": {"effort": "medium"}})
    return response.value


def zitat_im_text(fundstelle: Fundstelle, spezifikation: dict) -> bool:
    for abschnitt in spezifikation["abschnitte"]:
        if abschnitt["abschnitt"] == fundstelle.abschnitt.strip("§ "):
            return fundstelle.zitat in abschnitt["text"]
    return False


@tool
async def extrahiere_angaben(
    document_version: Annotated[str, Field(description="Version der Spezifikation SPEC-001: 1 oder 2")],
) -> list[dict] | dict:
    """Liest die Spezifikation SPEC-001 in einer Version und liefert zu R-01 bis R-06 die Fundstellen
    mit Abschnitt, Zitat und Werten. im_text sagt, ob das Zitat wirklich im genannten Abschnitt steht."""
    spezifikation = lade_spezifikation(document_version)
    if "fehler" in spezifikation:
        return spezifikation
    client = FoundryChatClient(project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                               model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"], credential=DefaultAzureCredential())
    extraktion = await extrahiere(Agent(client=client, name="Extraktion", instructions=ANWEISUNG), document_version)
    return [
        {**angabe.model_dump(),
         "fundstellen": [{**f.model_dump(), "im_text": zitat_im_text(f, spezifikation)} for f in angabe.fundstellen]}
        for angabe in extraktion.angaben
    ]
