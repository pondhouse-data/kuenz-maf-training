# Ü10 · Gesprächsverlauf und Middleware

Ein Modell merkt sich zwischen zwei Aufrufen nichts. Damit Folgefragen funktionieren, muss bei
jeder Frage der bisherige Gesprächsverlauf mitgeschickt werden. Das übernimmt hier der
Responses-Server. Mit **Middleware** siehst du, welches Tool der Agent wann aufruft und wie lange es dauert.

**Ausgangspunkt:** dein Projekt nach Ü9 (`main.py`, `tools.py`, `test_tools.py`).

## Schritt 1 · Ein Gespräch über den Server

Frag im Agent Inspector nacheinander: „Was gilt für R-03 bei A-100?“ und dann
„Und was steht dazu in Version 1 der Spezifikation?“. Der Agent versteht das „dazu“.

Klick auf **Clear Chat** und stell nur die zweite Frage. Jetzt beginnt ein neues Gespräch:
Der Agent weiß nicht, worauf sich „dazu“ bezieht, und fragt nach.

```text
Erkläre mir anhand von #file:main.py: Woher kennt der Agent bei der Folgefrage
das bisherige Gespräch? Was speichert der ResponsesHostServer (Microsoft Agent Framework 1.21),
und was ändert sich mit Clear Chat?
```

## Schritt 2 · Toolaufrufe sichtbar machen

```text
Ergänze in #file:main.py eine Middleware mit @function_middleware aus agent_framework,
die bei jedem Toolaufruf Toolname und Dauer ausgibt, z. B. "  [Tool lade_anforderungskatalog, 0.00 s]".
Gib sie dem Agenten mit middleware=[...].
```

Neu starten und eine Frage stellen. Im Terminal des Servers siehst du jetzt bei jeder Frage,
welche Tools das Modell aufruft. Setz zusätzlich einen Breakpoint auf `await call_next()`
und frag noch einmal: Der Debugger hält vor dem Tool an, im Fenster **Variables** steht `context`.

## Code verstehen

1. **Was ist neu?** Wo hängt die Middleware am Agenten, wo entsteht der Gesprächsverlauf?
2. **Welche Eingaben?** Was bekommt die Middleware (`context`) und was ist `call_next`?
3. **Was kommt zurück?** Was passiert, wenn die Middleware `call_next()` nicht aufruft?
4. **Was passiert bei Fehlern?** Was gibt die Middleware aus, wenn ein Tool einen Fehler liefert?
