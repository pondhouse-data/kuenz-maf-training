# Ü9 · Tools

Dein Agent aus Ü8 kennt nur, was das Modell weiß. Hier bekommt er **Tools**:
Python-Funktionen, die er aufrufen darf, um Daten zu laden. Danach beantwortet
er Fragen zu Prüfaufträgen, Anforderungen und zur Spezifikation aus unseren Daten.

**Ausgangspunkt:** dein Projekt aus Ü8. Alle Befehle im Terminal im Projektordner
`pruefagent/src/agent-framework-agent-basic-responses`.

## Schritt 0 · Daten ins Projekt kopieren

```bash
cp -r /workspaces/kuenz-maf-training/daten .
```

Die Daten sind synthetisch. Sie liegen jetzt in `daten/` neben `main.py` und werden später mit bereitgestellt.

## Schritt 1 · Ein Hello-World-Tool

Prompt an Copilot:

```text
Füge in #file:main.py ein Tool aktuelle_uhrzeit hinzu, das die aktuelle Uhrzeit
als Text "HH:MM" zurückgibt. Verwende den Decorator @tool aus agent_framework
(Microsoft Agent Framework 1.21) und einen kurzen Docstring. Übergib das Tool dem Agenten mit tools=[...].
```

Debug-Lauf neu starten und im Agent Inspector vergleichen: „Wie spät ist es?“ und „Was ist ein Agent?“

Bei der ersten Frage ruft das Modell das Tool auf, bei der zweiten nicht. Der Inspector zeigt den
Toolaufruf mit Argumenten und Ergebnis direkt im Chat. Das Modell entscheidet anhand von Name und
Docstring, ob es ein Tool braucht.

## Schritt 2 · Die drei Daten-Tools

Prompt an Copilot:

```text
Lege die Datei tools.py neben #file:main.py an. Verschiebe aktuelle_uhrzeit dorthin und schreibe drei weitere Tools
mit @tool aus agent_framework. Die Daten liegen im Ordner daten neben tools.py:
- lade_pruefauftrag(review_id) sucht in #file:daten/pruefauftraege.json den Auftrag mit dieser review_id.
- lade_anforderungskatalog(asset_id, requirement_id=None) gibt die Anforderungen aus
  #file:daten/anforderungskatalog.json zurück, auf Wunsch nur eine einzelne Anforderung.
- lade_spezifikation(document_version) lädt daten/spezifikation_v1.json bzw. daten/spezifikation_v2.json.
Bestimme den Datenordner relativ zu tools.py, nicht zum Arbeitsverzeichnis.
Beschreibe jeden Parameter und jedes Tool mit einem Docstring.
Gibt es eine ID oder Version nicht, gib {"fehler": "..."} zurück statt eine Ausnahme zu werfen.
Halte den Code einfach. Importiere die Tools in main.py, übergib alle vier dem Agenten,
nenne ihn PruefAgent und ändere die Instructions: Fragen nur mit den Tools beantworten,
bei einem Fehler nichts erfinden.
```

Neu starten und im Agent Inspector fragen:

- „Was gilt für R-03 bei A-100?“
- „Welche Spezifikation gehört zu PR-201?“
- „Was steht in PR-999?“

Erwartet: R-03 verlangt Protokollversion 2.0 · PR-201 gehört zu SPEC-001 Version 2 ·
PR-999 gibt es nicht. Der Wortlaut variiert. Klapp die Toolaufrufe auf: Welche Argumente hat
das Modell übergeben, was kam zurück?

## Schritt 3 · Ein paar Tests

```text
Schreibe test_tools.py mit drei bis vier kurzen pytest-Tests für #file:tools.py:
PR-001 gehört zu Version 1, ein unbekannter Auftrag liefert "fehler", R-03 einzeln laden, Version 2 laden.
```

```bash
uv run pytest
```

Lass dir die Tests danach erklären:

```text
Erkläre mir jeden Test in #file:test_tools.py in einem Satz: Was prüft er, und wann schlägt er fehl?
```

## Code verstehen, bevor du ihn übernimmst

Lies jeden Vorschlag, bevor du ihn annimmst, und beantworte für jedes Tool:

1. **Was ist neu?** Welche Zeilen hat Copilot geändert oder angelegt?
2. **Welche Eingaben?** Welche Parameter, und was sieht das Modell davon (Name, Docstring, Beschreibung)?
3. **Was kommt zurück?** Wie sieht das Ergebnis für PR-001 aus?
4. **Was passiert bei Fehlern?** Was bekommt das Modell bei PR-999?

Kannst du eine Frage nicht beantworten, frag Copilot: „Erkläre mir Zeile für Zeile, was … macht.“
