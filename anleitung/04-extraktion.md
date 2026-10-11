# Ü11 A · Strukturierte Ausgabe

Für die Prüfung soll das Modell nicht frei antworten, sondern **Angaben in einem
festen Schema** liefern: je Anforderung die Fundstellen mit Abschnitt, wörtlichem
Zitat und Wert. Ob eine Anforderung erfüllt ist, entscheidet danach der Code (Ü11 B).

**Ausgangspunkt:** dein Projekt nach Ü10.

## Schritt 1 · Das Schema und die Extraktion

```text
Lege extraktion.py neben #file:main.py an (Microsoft Agent Framework 1.21). Ein Agent ohne Tools liest eine Version
der Spezifikation und liefert zu jeder Anforderung R-01 bis R-06 die Fundstellen: Abschnitt, wörtliches Zitat
und die gefundenen Werte. Er bewertet nicht. Nur bei R-06 schlägt er "erfüllt", "abweichend" oder "unklar" vor,
mit Begründung.
- Die Antwort kommt in einem festen Schema (Pydantic, response_format), nicht als freier Text.
- Im Prompt stehen die Anforderungen von A-100 und der ganze Text der Spezifikation samt Anhang.
  Hol beides mit den Funktionen aus #file:tools.py.
- Anweisung an den Agenten: nur den gelieferten Text verwenden, wörtlich zitieren, bei unterschiedlichen
  Werten alle Fundstellen liefern, nichts erfinden. Werte als Liste ohne Einheit, z. B. ["DE","EN"], ["41"], ["1.4"], ["-20","40"].
- Das Modell soll gründlich lesen (reasoning effort medium).
- Prüfe im Code, ob jedes Zitat wirklich im genannten Abschnitt steht.
- Stelle die Extraktion als async Tool extrahiere_angaben(document_version) mit @tool bereit. Es liefert
  je Anforderung die Fundstellen, jede mit im_text true oder false. Eine unbekannte Version liefert den
  Fehler von lade_spezifikation.
Baue den Client so auf wie in #file:main.py und gib das Tool dort dem PruefAgent.
```

Neu starten und im Agent Inspector fragen: „Welche Fundstellen hat Version 2 zu R-04?“ und
„Welche Fundstellen hat Version 1 zu R-05?“. Klapp den Aufruf von `extrahiere_angaben` auf:
Dort steht das ganze Ergebnis der Extraktion, je Fundstelle mit `im_text`.

Erwartet für Version 2 bei R-04 **zwei** Fundstellen: §4.1 mit 30 ms und §A.1 mit 80 ms.
Die Spezifikation widerspricht sich hier. Für Version 1 liefert das Modell bei R-05 entweder keine
Fundstelle oder §6.3 mit einer Raumtemperatur. §6.3 betrifft das Bedienpult, nicht den Kran;
in Ü11 B sortiert die Regel solche Fundstellen aus.

## Code verstehen

1. **Was ist neu?** Wo steht das Schema, wo wird es dem Modell übergeben?
2. **Welche Eingaben?** Was steht im Prompt, was in den Instructions des Agenten?
3. **Was kommt zurück?** Was ist `response.value`, was `response.text`?
4. **Was passiert bei Fehlern?** Was steht im Toolergebnis, wenn das Modell ein Zitat erfindet?

Das Schema erzwingt die **Form** der Antwort, nicht ihre **Wahrheit**. Deshalb prüft der Code die Zitate.
