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

## Übung 16: Copilot-Studio-Agent im Ordner `ue16/`

- `ue16/` enthält den eigenen Dispatcher des Teilnehmers, geklont mit `pac copilot clone` (Topics und Tools als `*.mcs.yml`, Agent Flows unter `workflows/<Name>-<UUID>/workflow.json` und `metadata.yml`). Der Ordner ist in `.gitignore`; dort nie committen.
- Transport nach Copilot Studio ist `pac copilot push --project-dir <Workspace>`. `pac copilot pack` und `pac solution import` gehören nicht dazu.
- Der vorhandene Flow „Rückruf anlegen“ unter `workflows/` und `actions/` ist das Formatbeispiel. Ihn und seine Registrierung nicht ändern.
- In der Dev-Umgebung nur den eigenen Agenten pushen und nur eigene, gerade erzeugte Flows aktivieren oder zur eigenen Solution hinzufügen. Keine Verbindungen anlegen oder ändern, nichts in Foundry ändern, keine Tokens ausgeben.
- Der Auftrag kommt aus dem Prompt auf dem Ü16-Blatt; Fehlermeldungen aus Topic checker und Testchat gibt der Teilnehmer wörtlich zurück.
