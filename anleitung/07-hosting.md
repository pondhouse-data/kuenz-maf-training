# Ü13 · Das Projekt als Hosted Agent bereitstellen

Dein Prüfworkflow läuft bisher lokal hinter `main.py`. Jetzt stellst du genau dieses Projekt
über **Foundry Toolkit → Deploy to Microsoft Foundry** in Foundry bereit. Deployment und Playground übernimmt VS Code.

**Ausgangspunkt:** dein Projekt nach Ü11 B (mit oder ohne Ü12).

## Schritt 1 · Lokal prüfen und Inhalt ansehen

F5, im Agent Inspector „Prüfe PR-001“ und „Prüfe PR-999“ senden. PR-001 liefert das Prüfergebnis
mit run_id, PR-999 JSON mit `fehler`. Stoppe den Debug-Lauf danach.

Bereitgestellt wird der Projektordner, den `azure.yaml` unter `project` nennt:
`main.py`, deine Module, `pyproject.toml`, `uv.lock` und `daten/`. Die Abhängigkeiten installiert Foundry
beim Bereitstellen aus den Projektdateien. `FOUNDRY_PROJECT_ENDPOINT` setzt der Foundry-Dienst in der Cloud
selbst; den Modellnamen gibt `azure.yaml` als Umgebungsvariable mit. Die Cloud verwendet die Identität des
Agenten; deine lokale Anmeldung wird nicht hochgeladen.

## Schritt 2 · Deployment in VS Code

1. Foundry Toolkit → **Developer Tools → Build → Deploy to Microsoft Foundry**.
2. **Foundry Project Setup**: Subscription `Kuenz Training 2026`, Project `kuenz-agents` → **Next**.
3. **Basics**: Deployment Method **Code**, Package Mode **Remote**, Deploy to **New agent**,
   Hosted Agent Name `kuenz-pruefung-trainingNN` (NN = deine Teilnehmernummer) → **Next**.
4. **Review + Deploy**: Python (Auto-detected), Python 3.13, Entry Point `python main.py`,
   0.5 CPU / 1.0 Gi → **Deploy**. Unten rechts erscheint „… is deployed successfully“.
5. Unter **My Resources → Agents → Hosted Agent → Details** den Laufstatus abwarten.
6. **Playground**: „Prüfe PR-001“, „Prüfe PR-201“, „Prüfe PR-999“ testen.
   Notiere Agentname, getestete Version, Endpunkt, response_id und run_id.

Eine neue Version wird mit **Existing agent** bereitgestellt. Die Versionsauswahl im Playground
ändert nur dessen Testaufrufe: **Automatic** und der spätere Dispatcher müssen ebenfalls den
vorgesehenen Stand liefern. Falls Automatic eine alte Version liefert, Endpoint-Routing
im Foundry-Portal auf die neue Version setzen und erneut prüfen.

## Schritt 3 · Gespeicherte Antwort mit dem SDK abrufen

Ein neuer Playground-Aufruf startet eine neue Prüfung. Ein GET mit der response_id liest
das gespeicherte Resultat ohne neue Prüfung. Aus dem Projekt-Client direkt abrufen;
Agentname muss zu dem Endpunkt passen, der die Response erzeugt hat:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(".env")
with AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                     credential=DefaultAzureCredential(), allow_preview=True) as project:
    with project.get_openai_client(agent_name="kuenz-pruefung-trainingNN") as client:
        response = client.responses.retrieve("response_id-aus-dem-Playground")
        print(response.id, response.status, response.output_text)
        print(response.model_dump().get("agent"))  # tatsächlicher Agentname und Version
```

Den kurzen Code führst du im Projektordner in `uv run python` aus.
Prüfe dieselbe response_id, dasselbe JSON und dieselbe run_id. Im gespeicherten GET nennt
`agent` den tatsächlichen Agentnamen und die Version; diese Version mit dem beabsichtigten
Deployment vergleichen. Technisch completed ist
noch keine menschliche Freigabe. Danach folgt die Agent-Evaluation im Toolkit/Foundry-Portal
und die Anbindung des Dispatchers.

## Code verstehen

1. Wie wird aus "Prüfe PR-001" die Auftrags-ID, und was ändert sich am Code zwischen lokal und Cloud?
2. Warum erzeugt `main.py` für jede Anfrage einen frischen Workflow?
3. Welche IDs liefert der Workflow, welche der Responses-Dienst?
4. Was wird gepackt, was bleibt privat, welche Identität läuft in der Cloud?

[Toolkit-Anleitung](https://code.visualstudio.com/docs/intelligentapps/hosted-agents) ·
[Hosting vorhandenen Codes](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-deploy-own-code?tabs=python-responses)
