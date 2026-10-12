# Ü11 B · Der Prüfworkflow

Jetzt wird aus den Bausteinen die Prüfung: ein **Workflow** aus vier festen
Schritten. Das Modell extrahiert, der Code vergleicht mit festen Regeln.

```
Auftrag laden → Angaben extrahieren → Regeln vergleichen → Ergebnis ausgeben
```

Den fertigen Workflow startest du wie bisher mit F5 und testest ihn im Agent Inspector.
An Tag 3 stellst du genau dieses Projekt in Ü13 als Hosted Agent in Foundry bereit.

**Ausgangspunkt:** dein Projekt nach Ü11 A.

## Schritt 1 · Die Regeln

Jede Anforderung im Katalog hat eine `vergleichsregel` (siehe `daten/anforderungskatalog.json`).

```text
Lege regeln.py neben #file:main.py an: einfacher Python-Code ohne Modellaufruf und ohne Klassen.
Hauptfunktion: bewerte(anforderung: dict, angabe: dict, spezifikation: dict) -> dict
- anforderung: ein Eintrag aus "requirements" in #file:daten/anforderungskatalog.json
- angabe: ein Eintrag aus "angaben", wie ihn #file:extraktion.py liefert (fundstellen mit abschnitt, zitat,
  werte als Liste von Texten; bewertung_vorschlag)
- spezifikation: Inhalt von #file:daten/spezifikation_v1.json (Liste "abschnitte" mit abschnitt, titel, text)
Rückgabe: {"requirement_id", "status": "erfüllt" | "abweichend" | "unklar", "begruendung": ein kurzer Satz,
"fundstellen": nur die gültigen Fundstellen}
Prüfe in dieser Reihenfolge:
1. Gültig ist eine Fundstelle nur, wenn ihr zitat im text ihres Abschnitts steht (Leerzeichen und "−"/"-"
   tolerant vergleichen) und Titel und Text des Abschnitts keinen Begriff aus
   anforderung["anwendbarkeit"]["ausschlussbegriffe"] enthalten (falls vorhanden).
2. Keine gültige Fundstelle → "unklar".
3. typ "fachliche_bewertung" → bewertung_vorschlag der Angabe (fehlt er: "unklar").
4. Gültige Fundstellen mit unterschiedlichen werte → "unklar".
5. Sonst nach vergleichsregel["typ"]: teilmenge (alle werte in "erlaubt"), maximum (Zahl ≤ grenzwert),
   version_mindestens (Version ≥ grenzwert, Teile als Zahlen: 2.10 ist größer als 2.9),
   bereich_innerhalb (werte = [Minimum, Maximum], beide innerhalb min und max; "+" und "−" beachten).
   Passt es → "erfüllt", sonst "abweichend".
Halte den Code kurz.
```

```text
Schreibe test_regeln.py mit drei kurzen pytest-Tests für #file:regeln.py mit echten
Zitaten aus der Spezifikation: R-03 mit Version 1.4 (§3.2, v1) ist abweichend; R-04 mit 30 ms (§4.1) und
80 ms (§A.1, v2) ist unklar; R-05 mit der Raumtemperatur aus §6.3 (v1) ist unklar.
```

```bash
uv run pytest test_regeln.py
```

## Schritt 2 · Der Workflow

```text
Lege workflow.py neben #file:main.py an: ein Workflow mit vier Schritten (Microsoft Agent Framework 1.21,
WorkflowBuilder und Executor):
Auftrag laden → Angaben extrahieren (#file:extraktion.py) → Regeln vergleichen
(#file:regeln.py) → Ergebnis ausgeben.
- Der erste Schritt bekommt list[Message] und sucht PR-xxx in der letzten Nachricht.
  Einen unbekannten Auftrag gibt er direkt als JSON mit "fehler" aus.
- Das Ergebnis ist ein JSON-Text mit review_id, run_id (UUID), asset_id, document_id, document_version,
  den Befunden und als klaerungspunkte allen Befunden, die nicht "erfüllt" sind.
- erstelle_workflow() baut mit FoundryChatClient und DefaultAzureCredential den Extraktionsagenten
  und einen frischen Workflow. erstelle_agent() gibt erstelle_workflow().as_agent(name="Spezifikationspruefung") zurück.
Ändere #file:main.py: Importiere erstelle_agent aus workflow und starte in main()
ResponsesHostServer(erstelle_agent, history_source="agent"). Übergib die Funktion, ruf sie nicht
selbst auf: Jede Anfrage bekommt einen frischen Workflow.
```

Debug-Lauf neu starten.
Im Agent Inspector „Prüfe PR-001“, „Prüfe PR-201“ und „Prüfe PR-999“ senden.

Erwartet: Klärungspunkte für PR-001: R-03 und R-05, für PR-201: R-04 und R-05. PR-999 liefert JSON mit `fehler`.

## Schritt 3 · Mit den Referenzbefunden vergleichen

```text
Schreibe test_referenz.py: ein pytest-Test für PR-001 und PR-201, der den Workflow über
erstelle_agent() aus #file:workflow.py mit "Prüfe <ID>" ausführt und den Status jeder
Anforderung mit #file:daten/referenzbefunde.json vergleicht. Lade vorher die .env. Ohne
FOUNDRY_PROJECT_ENDPOINT wird der Test übersprungen.
```

```bash
uv run pytest test_referenz.py -v
```

Erwartet: zwei bestandene Tests. Der Test ruft das Modell auf und dauert etwa eine halbe Minute.

## Code verstehen

1. **Was ist neu?** Welche vier Schritte gibt es, und wie hängen sie zusammen?
2. **Welche Eingaben?** Was reicht jeder Schritt an den nächsten weiter?
3. **Was kommt zurück?** Wie sieht das Ergebnis aus, und welche Teile sind Klärungspunkte?
   Warum baut der Server für jede Anfrage einen frischen Workflow?
4. **Was passiert bei Fehlern?** Was wird aus R-04, wenn die Extraktion §A.1 übersieht?
