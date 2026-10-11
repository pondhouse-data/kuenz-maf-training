# Hinweise für Coding-Agenten

Dies ist ein **Trainings-Repository**. Teilnehmer erzeugen mit dem offiziellen Foundry Toolkit ein
Agentenprojekt im Ordner `pruefagent/` und bauen es Schritt für Schritt mit dem Microsoft Agent Framework
aus. Den Code schreiben sie mit deiner Hilfe selbst.

## Aufbau

- `README.md` und `anleitung/` beschreiben die Schritte Ü8 bis Ü13.
- `daten/` enthält synthetische Fachdaten. Teilnehmer kopieren den Ordner in ihr Projekt.
- Das Projekt liegt in `pruefagent/src/agent-framework-agent-basic-responses/` (`main.py`, `pyproject.toml`, `.env`).

## Regeln

- Arbeite im Projektordner des Teilnehmers und ändere nur, was die Anfrage verlangt.
- Behalte den Aufbau des offiziellen Samples bei: `main.py` startet den `ResponsesHostServer`.
- Verwende die festgelegten Paketversionen aus `pyproject.toml` (Microsoft Agent Framework 1.21).
- Schreibe den Code neu aus der Anfrage und den angehängten Dateien, so wie ihn der Teilnehmer verstehen soll.
