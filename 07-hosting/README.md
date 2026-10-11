# 07 · Der Prüfworkflow als Hosted Agent

Der Prüfworkflow aus 05 läuft bisher lokal hinter `main.py`. Jetzt stellst du denselben Code
über **Foundry Toolkit → Code → Remote** in Foundry bereit. Deployment und Playground übernimmt VS Code.

**Ausgangspunkt:** fertiger Workflow aus 05 samt `main.py`, im Checkpoint07 vorbereitet.

## Schritt 1 · Lokal prüfen

**Run and Debug → Debug Local Agent HTTP Server → F5** → `07-hosting`. Im Agent Inspector
„Prüfe PR-001“ und „Prüfe PR-999“ senden. PR-001 liefert das Prüfergebnis mit run_id,
PR-999 JSON mit `fehler`. Stoppe den Debug-Lauf danach.

## Schritt 2 · Vollständigen Quellordner prüfen

Öffne **07-hosting als Workspace** in VS Code. Wähle die bestehende root `.venv` als Interpreter.
`azure.yaml` liegt direkt in07, `services.pruefung.project` ist `.`: nur07 wird gepackt.
`main.py`, Workflowmodule, `requirements.txt` und `daten/` müssen dort liegen.
Die synthetischen Daten sind bereits kopiert; `tools.py` lädt diese lokale daten-Mappe.
Bei eigenen Datenänderungen root und07 synchron halten.

Im Terminal in07:

```bash
uv sync --locked
cp ../.env .env
```

Prüfe FOUNDRY_PROJECT_ENDPOINT und AZURE_AI_MODEL_DEPLOYMENT_NAME=training-chat.
Der Modellname ist in `azure.yaml` als Cloud-Umgebung deklariert.
FOUNDRY_PROJECT_ENDPOINT setzt der Foundry-Dienst in der Cloud automatisch;
für lokale Aufrufe steht er in deiner .env. Der Name ist als Deployment-Umgebungsvariable reserviert.
Private .env, virtuelle Umgebung und Caches werden über `.agentignore` ausgeschlossen.
Die Cloud verwendet die Identität des Agenten; deine lokale Anmeldung wird nicht hochgeladen.

## Schritt 3 · Deployment in VS Code

1. Foundry Toolkit → **Developer Tools → Build → Deploy to Microsoft Foundry**.
2. Bestehendes Trainingsprojekt auswählen. **Code → Remote → New agent**.
3. Eigener Name `kuenz-pruefung-trainingNN` (NN=deine Teilnehmernummer).
4. Review: Python 3.13, Startbefehl `python3 main.py`, Quelle07-hosting,0.5CPU,1GiB.
5. **Deploy**. Unter **My Resources → Agents → Hosted Agent → Details** den Laufstatus abwarten.
6. **Playground**: „Prüfe PR-001“, „Prüfe PR-201“, „Prüfe PR-999“ testen.
   Notiere Agentname, getestete Version, Endpunkt, response_id und run_id.

Eine neue Version wird mit **Existing agent** bereitgestellt. Die Versionsauswahl im Playground
ändert nur dessen Testaufrufe: **Automatic** und der spätere Dispatcher müssen ebenfalls den
vorgesehenen Stand liefern. Falls Automatic eine alte Version liefert, Endpoint-Routing
im Foundry-Portal auf die neue Version setzen und erneut prüfen.

## Schritt 4 · Gespeicherte Antwort mit dem SDK abrufen

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

Du kannst den kurzen Code im Python-Terminal ausführen; ein eigenes Hilfsskript ist nicht nötig.
Prüfe dieselbe response_id, dasselbe JSON und dieselbe run_id. Im gespeicherten GET nennt
`agent` den tatsächlichen Agentnamen und die Version; diese Version mit dem beabsichtigten
Deployment vergleichen. Technisch completed ist
noch keine menschliche Freigabe. Danach folgt die Agent-Evaluation im Toolkit/Foundry-Portal
und die Anbindung des Dispatchers.

## Code verstehen

1. Wie wird aus "Prüfe PR-001" die Auftrags-ID, und was ändert sich am Code zwischen lokal und Cloud?
2. Warum eine Factory pro Request statt eines gemeinsam genutzten Workflows?
3. Welche IDs liefert der Workflow, welche der Responses-Dienst?
4. Was wird gepackt, was bleibt privat, welche Identität läuft in der Cloud?

[Toolkit-Anleitung](https://code.visualstudio.com/docs/intelligentapps/hosted-agents) ·
[Hosting vorhandenen Codes](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-deploy-own-code?tabs=python-responses)
