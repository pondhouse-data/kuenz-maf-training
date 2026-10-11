# Ü10 · Gesprächsverlauf und Middleware

Ein Modell merkt sich zwischen zwei Aufrufen nichts. Damit Folgefragen funktionieren, muss bei
jeder Frage der bisherige Gesprächsverlauf mitgeschickt werden. Das übernimmt hier der
Responses-Server. Mit **Middleware** siehst du, welches Tool der Agent wann aufruft und wie lange es dauert.

**Ausgangspunkt:** dein Projekt nach Ü9 (`main.py`, `tools.py`, `test_tools.py`).

## Schritt 1 · Mit und ohne Session

Für jede Unterhaltung führt der Responses-Server eine **Session** (`AgentSession`) mit dem bisherigen Verlauf.

**Mit Session:** Frag im Agent Inspector nacheinander „Was gilt für R-03 bei A-100?“ und dann
„Und was steht dazu in Version 1 der Spezifikation?“. Beide Fragen laufen in derselben Session;
der Agent versteht das „dazu“.

**Ohne Session:** Klick auf **Clear Chat** und stell nur die zweite Frage. Jetzt beginnt eine neue, leere
Session: Der Agent weiß nicht, worauf sich „dazu“ bezieht, und fragt nach.

```text
Erkläre mir anhand von #file:main.py: Woher kennt der Agent bei der Folgefrage
das bisherige Gespräch? Was speichert der ResponsesHostServer (Microsoft Agent Framework 1.21),
und was ändert sich mit Clear Chat?
```

## Schritt 2 · Toolaufrufe sichtbar machen

```text
Ergänze in #file:main.py zwei Middlewares aus agent_framework und gib sie dem Agenten mit middleware=[...]:
- @function_middleware: gibt bei jedem Toolaufruf Toolname und Dauer aus, z. B. "  [Tool lade_anforderungskatalog, 0.00 s]".
- @chat_middleware: gibt vor jedem Modellaufruf die Zahl der Nachrichten aus, z. B. "  [Modellaufruf mit 5 Nachrichten]".
```

Neu starten. Im Terminal **Run Agent HTTP Server** siehst du jetzt bei jeder Frage, welche Tools das Modell
aufruft und wie viele Nachrichten es bekommt. Wiederhole Schritt 1: Mit Session bekommt das Modell bei der
Folgefrage den bisherigen Verlauf mit (zum Beispiel 5 Nachrichten), nach **Clear Chat** nur deine Frage (1 Nachricht).

## Code verstehen

1. **Was ist neu?** Wo hängt die Middleware am Agenten, wo entsteht der Gesprächsverlauf?
2. **Welche Eingaben?** Was bekommen die beiden Middlewares (`context`) und was ist `call_next`?
3. **Was kommt zurück?** Was passiert, wenn die Middleware `call_next()` nicht aufruft?
4. **Was passiert bei Fehlern?** Was gibt die Middleware aus, wenn ein Tool einen Fehler liefert?
