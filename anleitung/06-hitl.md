# Ü12 · Ein Mensch entscheidet (optional)

Bei Klärungspunkten soll ein Prüfer entscheiden, bevor das Ergebnis weitergeht.
Der Workflow **hält an**, fragt je Klärungspunkt nach und läuft mit den Antworten weiter.
Die Entscheidung des Menschen wird getrennt vom KI-Befund gespeichert.

**Ausgangspunkt:** dein Projekt nach Ü11 B.
Diese Übung läuft im Terminal: Der Workflow stellt seine Fragen dort, du antwortest mit der Tastatur.
Der Prüfworkflow hinter `main.py` bleibt unverändert; nur der Terminalaufruf bekommt den Prüfer.

## Schritt 1 · Den Prüfer einbauen

```text
Erweitere #file:workflow.py (Microsoft Agent Framework 1.21) um eine Prüfung mit menschlicher Entscheidung.
erstelle_agent() und der bisherige Workflow bleiben unverändert.
- Neuer Schritt Pruefer: Er fragt für jeden Befund, der nicht "erfüllt" ist, mit ctx.request_info nach
  und läuft mit @response_handler weiter, sobald alle Antworten da sind.
- Ein eigener Workflow verwendet die vorhandenen Schritte, setzt Pruefer nach dem Vergleich ein und gibt das
  Ergebnis wie bisher aus, ergänzt um die Entscheidungen getrennt von den Befunden als "entscheidungen".
- Eine async main() mit der Auftrags-ID als Argument: diesen Workflow mit [Message("user", ["Prüfe <ID>"])]
  streamen und die request_info-Ereignisse nach request_id sammeln. Zu jeder Frage Befund und Fundstellen
  zeigen und die Entscheidung mit input() abfragen. Danach denselben Workflow mit
  workflow.run(responses=antworten) fortsetzen und das Ergebnis als JSON ausgeben.
```

```bash
uv run python workflow.py PR-101
```

Nimm statt PR-101 deinen eigenen Prüfauftrag (PR-101 bis PR-105). Erwartet: zwei Fragen
(R-03 und R-05) und im Ergebnis deine beiden Entscheidungen unter `entscheidungen`.
Prüf danach, dass der Prüfworkflow hinter `main.py` unverändert ist; genau ihn stellst du in Ü13 bereit:
F5, im Agent Inspector „Prüfe PR-001“. Erwartet wie in Ü11 B: Klärungspunkte R-03 und R-05, keine Rückfrage,
kein `entscheidungen`.

## Code verstehen

1. **Was ist neu?** Wo hält der Workflow an, wo läuft er weiter?
2. **Welche Eingaben?** Was sieht der Prüfer, was gibt er zurück?
3. **Was kommt zurück?** Wo stehen KI-Befund und menschliche Entscheidung im Ergebnis?
4. **Was passiert bei Fehlern?** Was passiert, wenn eine Antwort fehlt?

Im Betrieb würde der Workflow seinen Stand speichern (Checkpoint) und erst Stunden später
weiterlaufen. In der Übung läuft alles in einem Prozess.
