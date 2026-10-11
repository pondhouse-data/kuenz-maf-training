# Künz Agententraining · Microsoft Agent Framework

Du erzeugst dein Agentenprojekt mit dem offiziellen **Foundry Toolkit** in VS Code und baust genau
dieses Projekt Schritt für Schritt aus: Tools, Gesprächsverlauf, Extraktion und ein Prüfworkflow.
Am Ende stellst du dasselbe Projekt in Microsoft Foundry bereit.

| Schritt | Aufgabe | Tag |
| --- | --- | --- |
| Ü8 · [Projekt erzeugen](#ü8--projekt-mit-dem-foundry-toolkit-erzeugen) | Offizielles Sample erzeugen, im Agent Inspector testen, Streaming verstehen | 2 |
| Ü9 · [Tools](anleitung/02-tools.md) | Tools für Prüfauftrag, Katalog und Spezifikation | 2 |
| Ü10 · [Gesprächsverlauf und Middleware](anleitung/03-session-middleware.md) | Folgefragen und sichtbare Toolaufrufe | 2 |
| Ü11 A · [Extraktion](anleitung/04-extraktion.md) | Angaben in einem festen Schema extrahieren, als Tool des Prüfagenten | 2 |
| Ü11 B · [Prüfworkflow](anleitung/05-workflow.md) | Extrahieren, Regeln vergleichen, Ergebnis ausgeben | 2 |
| Ü12 · [Ein Mensch entscheidet](anleitung/06-hitl.md) | Optional: menschliche Entscheidung je Klärungspunkt, im Terminal | 3 |
| Ü13 · [Bereitstellen](anleitung/07-hosting.md) | Das Projekt über VS Code in Foundry bereitstellen | 3 |

## Umgebung öffnen

[Eigenen Codespace öffnen](https://codespaces.new/pondhouse-data/kuenz-maf-training?quickstart=1).
Dafür brauchst du einen persönlichen GitHub-Account mit verfügbarem Codespaces-Kontingent.
Die Umgebung richtet Python 3.13, uv, Azure CLI, Python-Debugger, GitHub Copilot und Foundry Toolkit ein.
Foundry Toolkit läuft im Codespace über den Remote-Erweiterungshost und ist im Browsereditor verfügbar.
Optional kannst du denselben Codespace über **… → Open in Visual Studio Code** in VS Code Desktop öffnen.

Fragt VS Code „Do you trust the authors of the files in this folder?“: **Trust Folder & Continue**.

Im Terminal anmelden, damit dein Code das Modell aufrufen darf:

```bash
az login --use-device-code --tenant 42abcb50-0ca4-44ec-b66c-80926c94af9d
```

Prüfe das angemeldete Trainingskonto. `az login` gilt für das Terminal und deinen Code;
Foundry Toolkit meldet dich im nächsten Schritt separat an.

## Ü8 · Projekt mit dem Foundry Toolkit erzeugen

1. Foundry Toolkit in der linken Leiste öffnen → **Developer Tools → Build → Create Agent**.
   Unter **Code an agent from samples** **Agent Framework** wählen. Vorlage: **Basic Hosted Agent**
   (Python · Agent Framework · Responses).
2. **Workspace Folder**: `/workspaces/kuenz-maf-training`, **Folder Name**: `pruefagent`.
3. **Environment Setup**: **Setup with Microsoft Foundry**. Fragt das Toolkit nach einer Anmeldung, mit dem
   Trainingskonto anmelden. **Subscription** `Kuenz Training 2026` → **Project Name** `kuenz-agents` →
   **Model Deployment** `training-chat` → **Create**. Kein neues Projekt und kein neues Modell anlegen.
4. VS Code öffnet den Ordner `pruefagent`. Die Frage nach dem Git-Repository im übergeordneten Ordner
   kannst du schließen. Der Agent liegt in `src/agent-framework-agent-basic-responses/main.py`; das ist ab jetzt
   dein **Projektordner**. Daneben liegt die `.env`, die das Toolkit mit `FOUNDRY_PROJECT_ENDPOINT` und
   `AZURE_AI_MODEL_DEPLOYMENT_NAME=training-chat` gefüllt hat.
5. Terminal öffnen und im Projektordner den im Training geprüften Paketstand festlegen. uv aktualisiert
   `pyproject.toml` und `uv.lock` und legt die `.venv` an:

   ```bash
   cd src/agent-framework-agent-basic-responses
   uv add agent-framework-core==1.21.0 agent-framework-foundry==1.14.1 agent-framework-foundry-hosting==1.0.0b261008 azure-ai-projects==2.6.1
   uv add --dev pytest==8.4.2
   ```

6. **Python: Select Interpreter** → **Enter interpreter path** →
   `/workspaces/kuenz-maf-training/pruefagent/src/agent-framework-agent-basic-responses/.venv/bin/python`.
7. **Run and Debug → Debug Local Agent HTTP Server → F5**. Der Server startet auf Port 8088,
   Agent Inspector öffnet sich. Frage: „Was ist ein Agent? Antworte in zwei Sätzen.“
8. Ändere die Instructions in `main.py` auf
   `"Du bist ein hilfreicher Assistent. Antworte kurz und auf Deutsch."`, speichere, stoppe den Debug-Lauf,
   starte mit F5 neu und vergleiche. Agent Inspector allein startet den Server nicht.

### Agent und Streaming verstehen

Im Agent Inspector erscheint die Antwort Stück für Stück. Unter **Events** siehst du die einzelnen
`response.output_text.delta`-Ereignisse: Der Server streamt die Antwort, sobald das Modell sie erzeugt.

```text
Erkläre mir #file:main.py Zeile für Zeile:
Client, Agent, Instructions und ResponsesHostServer. Wie kommt eine Frage aus dem Agent Inspector
zum Agenten, und wo wird die Antwort gestreamt?
```

## Ab Ü9 · Im eigenen Projekt weiterarbeiten

Alle weiteren Schritte ändern dasselbe Projekt. Gestartet wird immer mit **F5**, getestet im
Agent Inspector. Nach einer Codeänderung den Debug-Lauf stoppen und neu starten.
Tests laufen im Terminal im Projektordner:

```bash
uv run pytest
```

Für die Prompts öffnest du Copilot Chat. `#file:…` hängt eine Datei an, damit Copilot sie sieht.

## Daten und Aufbewahren

`daten/` enthält synthetische Prüfaufträge, Anforderungen, Spezifikationen und Referenzbefunde.
Im Betrieb kämen diese aus ERP, Dataverse, SharePoint beziehungsweise einer Dokumentextraktion.
`referenzbefunde.json` enthält menschlich geprüfte Sollbefunde. In Ü9 kopierst du den Ordner in deinen
Projektordner, damit er beim Bereitstellen mitkommt.

Speichere deine Dateien. Auf https://github.com/codespaces am Tagesende **… → Stop codespace** wählen.
Dateien und Anmeldung bleiben erhalten. Vor dem Löschen eigene Projektdateien herunterladen;
private `.env` und Anmeldung gehören nicht in eine weitergegebene Kopie.
Nach dem Training erzeugst du eigene Projekte genauso über das offizielle Toolkit.

[Offizieller Bootstrap, lokaler Test und Deployment](https://code.visualstudio.com/docs/intelligentapps/hosted-agents).
