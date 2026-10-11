# 05 · Der Prüfworkflow

Jetzt wird aus den Bausteinen die Prüfung: ein **Workflow** aus vier festen
Schritten. Das Modell extrahiert, der Code vergleicht mit festen Regeln.

```
Auftrag laden → Angaben extrahieren → Regeln vergleichen → Ergebnis ausgeben
```

Den fertigen Workflow startest du wie bisher mit F5 und testest ihn im Agent Inspector.
An Tag 3 stellst du genau diesen Code in Schritt 07 als Hosted Agent in Foundry bereit.

**Ausgangspunkt:** der fertige Stand aus 04.

## Schritt 1 · Die Regeln

Jede Anforderung im Katalog hat eine `vergleichsregel` (siehe `daten/anforderungskatalog.json`).

```text
Lege 05-workflow/regeln.py an: einfacher Code ohne Modellaufruf. Eine Funktion bewerte vergleicht eine Angabe
aus #file:05-workflow/extraktion.py mit ihrer Anforderung aus #file:daten/anforderungskatalog.json und liefert
den Befund: Status "erfüllt", "abweichend" oder "unklar" mit einer kurzen Begründung als Satz.
- Es zählen nur Fundstellen, deren Zitat wirklich im genannten Abschnitt steht (Leerzeichen und Minuszeichen
  tolerant vergleichen) und deren Abschnitt keinen Ausschlussbegriff der Anforderung enthält.
- Keine gültige Fundstelle oder unterschiedliche Werte → "unklar".
- Sonst gilt die vergleichsregel der Anforderung. Bei fachliche_bewertung zählt der Vorschlag des Modells.
- Versionsnummern als Zahlen vergleichen: 2.10 ist größer als 2.9.
```

```text
Schreibe in 05-workflow/test_regeln.py drei kurze pytest-Tests für #file:05-workflow/regeln.py mit echten
Zitaten aus der Spezifikation: R-03 mit Version 1.4 (§3.2, v1) ist abweichend; R-04 mit 30 ms (§4.1) und
80 ms (§A.1, v2) ist unklar; R-05 mit der Raumtemperatur aus §6.3 (v1) ist unklar.
```

```bash
uv run pytest 05-workflow
```

## Schritt 2 · Der Workflow

```text
Lege 05-workflow/workflow.py an: ein Workflow mit vier Schritten (Microsoft Agent Framework 1.21,
WorkflowBuilder und Executor):
Auftrag laden → Angaben extrahieren (#file:05-workflow/extraktion.py) → Regeln vergleichen
(#file:05-workflow/regeln.py) → Ergebnis ausgeben.
- Der erste Schritt bekommt list[Message] und sucht PR-xxx in der letzten Nachricht.
  Einen unbekannten Auftrag gibt er direkt als JSON mit "fehler" aus.
- Das Ergebnis ist ein JSON-Text mit review_id, run_id (UUID), asset_id, document_id, document_version,
  den Befunden und als klaerungspunkte allen Befunden, die nicht "erfüllt" sind.
- erstelle_workflow() baut mit FoundryChatClient und DefaultAzureCredential den Extraktionsagenten
  und einen frischen Workflow. erstelle_agent() gibt erstelle_workflow().as_agent(name="Spezifikationspruefung") zurück.
Ändere #file:05-workflow/main.py: Importiere erstelle_agent aus workflow, rufe load_dotenv() auf und starte
ResponsesHostServer(erstelle_agent, history_source="agent").run(). Übergib die Funktion, ruf sie nicht
selbst auf: Jede Anfrage bekommt einen frischen Workflow.
```

Starten: **Run and Debug → Debug Local Agent HTTP Server → F5** → `05-workflow`.
Im Agent Inspector „Prüfe PR-001“, „Prüfe PR-201“ und „Prüfe PR-999“ senden.

Erwartet: Klärungspunkte für PR-001: R-03 und R-05, für PR-201: R-04 und R-05. PR-999 liefert JSON mit `fehler`.

## Schritt 3 · Mit den Referenzbefunden vergleichen

```text
Schreibe 05-workflow/test_referenz.py: ein pytest-Test für PR-001 und PR-201, der den Workflow über
erstelle_agent() aus #file:05-workflow/workflow.py mit "Prüfe <ID>" ausführt und den Status jeder
Anforderung mit #file:daten/referenzbefunde.json vergleicht. Lade vorher die .env. Ohne
FOUNDRY_PROJECT_ENDPOINT wird der Test übersprungen.
```

```bash
uv run pytest 05-workflow/test_referenz.py -v
```

Erwartet: zwei bestandene Tests. Der Test ruft das Modell auf und dauert etwa eine halbe Minute.

## Code verstehen

1. **Was ist neu?** Welche vier Schritte gibt es, und wie hängen sie zusammen?
2. **Welche Eingaben?** Was reicht jeder Schritt an den nächsten weiter?
3. **Was kommt zurück?** Wie sieht das Ergebnis aus, und welche Teile sind Klärungspunkte?
   Warum baut der Server für jede Anfrage einen frischen Workflow?
4. **Was passiert bei Fehlern?** Was wird aus R-04, wenn die Extraktion §A.1 übersieht?

## Nicht fertig geworden?

Der Ordner `06-hitl` startet mit unserem fertigen Stand dieses Schritts.
