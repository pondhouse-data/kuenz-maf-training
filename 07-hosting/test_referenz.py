"""Vergleicht den Prüfworkflow mit den menschlich geprüften Referenzbefunden. Ruft das Modell auf.

Starten im Projekt-Hauptordner (nach az login):
    uv run pytest 07-hosting/test_referenz.py -v
"""
import asyncio
import json
import os

import pytest
from dotenv import load_dotenv

from tools import lade_json
from workflow import erstelle_agent

load_dotenv()
pytestmark = pytest.mark.skipif(not os.getenv("FOUNDRY_PROJECT_ENDPOINT"), reason="keine .env: Modellaufruf übersprungen")


@pytest.mark.parametrize("review_id", ["PR-001", "PR-201"])
def test_befunde_wie_referenz(review_id):
    response = asyncio.run(erstelle_agent().run(f"Prüfe {review_id}"))
    ergebnis = json.loads(response.text)
    pruefung = next(p for p in lade_json("referenzbefunde.json")["pruefungen"] if review_id in p["review_ids"])
    soll = {b["requirement_id"]: b["status"] for b in pruefung["befunde"]}
    assert {b["requirement_id"]: b["status"] for b in ergebnis["befunde"]} == soll
