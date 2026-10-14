# Ü16 · Auftrag an GitHub Copilot: Freigabe der Klärungspunkte

Du bist mein Coding-Agent im Codespace. Baue in meinem geklonten Copilot-Studio-Agenten die Freigabe der Klärungspunkte: zwei Agent Flows und zwei Topics. Arbeite selbstständig: Dateien schreiben, Terminalbefehle ausführen, echte Ausgaben lesen, eigene Fehler beheben, erneut pushen. Melde dich erst, wenn Push und Aktivierung tatsächlich funktioniert haben.

## Meine Werte

Die Werte stehen in meiner Chat-Nachricht: Workspace (mit `pac copilot clone` geklont), Schemaname des Agenten, Vorname, Unique name meiner Solution, Name der HTTP-Verbindungsreferenz meiner Prüf-Topics, mein Hosted Agent. Außerdem gilt:

- Dev-Umgebung: https://kuenztraining2026.crm4.dynamics.com
- Dataverse-Verbindungsreferenz (Display name): Freigabe Dataverse <Vorname>
- Approvals-Verbindungsreferenz (Display name): Freigabe Approvals <Vorname>
- Neue Flows und Tools tragen den Zusatz <Vorname>, die Topics nicht.

## Grenzen

- Lies `AGENTS.md` und diesen Auftrag im Repo-Wurzelverzeichnis. Schreibe und lies Dateien sonst nur im Workspace aus meiner Nachricht. Anleitungen deines eigenen Agent-Clients darfst du lesen; andere Trainings-, Lösungs- oder Nachweisdateien sind keine Quelle. Kein Git-Commit, kein Git-Push. `pac copilot pack` gehört nicht zu diesem Weg; Transport ist `pac copilot push --project-dir <Workspace>`.
- In Dev nur meinen eigenen Agenten (Schemaname aus meiner Nachricht) pushen und pullen. Per Dataverse-Web-API darfst du lesen: eigene Objekte dieses Agenten, meine Verbindungsreferenzen und die Metadaten der Tabelle `kt_freigabe`. Token intern über `az account get-access-token --resource https://kuenztraining2026.crm4.dynamics.com`; Token nie ausgeben oder speichern.
- Ändern darfst du nur: deine neuen Flows aktivieren (statecode 1, statuscode 2), ihre Fehlermeldungen lesen und sie meiner Solution hinzufügen (`pac solution add-solution-component`, Komponententyp 29). Hast du wegen einer nicht übernommenen Definition einen Flow mit neuer UUID ersetzt, darfst du die ersetzte, **von dir in diesem Auftrag erzeugte** Version deaktivieren und löschen, sobald die neue zurückgelesen und aktiv ist; vorher prüfen, dass die UUID nicht schon beim Klonen da war. Ihren alten Wrapper entfernst du ebenfalls. Keine Verbindungen anlegen oder ändern, keine fremden Objekte, keine Zeilen direkt schreiben, nichts in Foundry.
- Der bestehende Flow „Rückruf anlegen“ und seine Tool-Registrierung bleiben unverändert. Er liegt im Clone unter `workflows/` und `actions/` und ist dein Formatbeispiel für einen nativen Agent Flow: `workflow.json`, `metadata.yml`, TaskDialog-Wrapper, `host.apiId`/`operationId`/`connectionName`, Response-Schema.

## Zuerst lesen

- Die vorhandenen Topics „Prüfauftrag prüfen“ und „Prüfstatus abrufen“ (unter `topics/`). Sie setzen die Globals `review_id`, `run_id`, `response_id`, `requester_id`, `agent_name`, `agent_version` und lesen Foundry über meine HTTP-Referenz. Diese Topics nicht ändern.
- `connectionreferences.mcs.yml`. Ermittle die logischen Namen meiner beiden neuen Referenzen „Freigabe Dataverse <Vorname>“ und „Freigabe Approvals <Vorname>“ per Web API (Tabelle `connectionreferences`, Feld `connectionreferencedisplayname`; meist `kt_FreigabeDataverse<Vorname>` und `kt_FreigabeApprovals<Vorname>`) und ergänze sie dort im vorhandenen Format, falls sie fehlen. Connector-IDs: `/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps` und `/providers/Microsoft.PowerApps/apis/shared_approvals`. Bestehende Einträge nicht ändern.
- Die Tabelle **Freigaben**: logischer Name `kt_freigabe`, EntitySet `kt_freigaben`, Primär-ID `kt_freigabeid`. Spalten per Metadaten prüfen: `kt_review_id`, `kt_run_id`, `kt_response_id`, `kt_requester_id`, `kt_agent_name`, `kt_agent_version`, `kt_technical_status`, `kt_klaerungspunkte`, `kt_entscheidung` (Choice: angefragt 582100000, freigegeben 582100001, abgelehnt 582100002), `kt_kommentar`, `kt_pruefer`, `kt_zeitpunkt`.

## 1. Topic „Klärungspunkte freigeben“

- Nur für die ausdrückliche Bitte, die Klärungspunkte des gespeicherten Laufs zur menschlichen Freigabe zu senden.
- Vorab abweisen („Bindung abgewiesen …“, Dialog beenden): fehlende Globals, `Global.requester_id` ≠ `System.User.Id`, mehrere oder eine andere PR-Nummer im Satz als `Global.review_id`, schon vorhandene `Global.approval_row_id`.
- Gespeicherte Foundry-Antwort selbst nachlesen, wie in „Prüfstatus abrufen“: GET `/api/projects/kuenz-agents/agents/<Global.agent_name>/endpoint/protocols/openai/responses/<Global.response_id>?api-version=v1` über meine HTTP-Referenz, Modus Maker. Bindung prüfen: `status` completed, `id` = response_id, `agent_reference.name` = agent_name, review_id und run_id aus dem JSON in `output[].content[]` (type `output_text`) stimmen, genau sechs Befunde. Klärungspunkte = nur die Befunde mit status ≠ „erfüllt“, als Text „requirement_id: status – begruendung“ je Zeile. Nichts erfinden.
- Frage nach der E-Mail-Adresse des menschlichen Prüfers.
- Danach echte Ja/Nein-Bestätigung: als Text erfassen (StringPrebuiltEntity), mit Trim/Lower normalisieren und ausdrücklich auf „ja“ und „nein“ verzweigen. BooleanPrebuiltEntity erkennt deutsches „Nein“ nicht zuverlässig.
- Nein: kurze Abbruchmeldung, kein Flow-Aufruf, Dialog beenden.
- Ja: genau einmal den Flow „Klärungspunkte freigeben <Vorname>“ aufrufen (InvokeFlowAction mit `input.binding` und skalarem `output.binding`) mit den sechs Globals, der Prüfer-Adresse und den Klärungspunkten. `Global.approval_row_id` aus der Antwort setzen.
- Nur wenn der Flow `status` = „Freigabe angefragt“ und eine nicht leere `approval_row_id` zurückgibt, sende genau diese Nachricht mit allen fünf Werten sichtbar: `Freigabe angefragt. Zeilen-ID: {Global.approval_row_id}. Prüfauftrag: {Global.review_id}. run_id: {Global.run_id}. response_id: {Global.response_id}. Der Prüfer entscheidet in Teams unter Genehmigungen.` Ein gesetzter Global allein reicht nicht; die Werte müssen im Testchat erscheinen. Sonst die echte Rückgabe als Fehler zeigen, nie eine Erfolgsmeldung erfinden. Danach alle Dialoge beenden.

## 2. Agent Flow „Klärungspunkte freigeben <Vorname>“

- Trigger „When an agent calls the flow“ mit acht Texteingaben: `review_id`, `run_id`, `response_id`, `requester_id`, `agent_name`, `agent_version`, `pruefer_email`, `klaerungspunkte`. Neuer Flow mit `modernFlowType: 1` und selbst erzeugter UUID.
- Leere Pflichteingaben: sofort „Respond to the agent“ mit status `Bindung abgewiesen`, approval_row_id leer.
- Genau eine Zeile in **Freigaben** anlegen (Dataverse-Referenz): alle Bindungsfelder, Klärungspunkte, `kt_technical_status` = `awaiting_human`, `kt_entscheidung` = angefragt. Scheitert das: status `Freigabe nicht angelegt`, keine Freigabe.
- SOFORT danach „Respond to the agent“ mit den Textausgaben `status` = `Freigabe angefragt` und `approval_row_id` = Primär-ID der Zeile. Erst danach die Freigabe starten. Die Antwort an den Agenten darf nie auf den Menschen warten.
- Klassische Freigabe „Start and wait for an approval“ (Approvals-Referenz): Approve/Reject – First to respond, an `pruefer_email`, Titel mit review_id und run_id, Details mit den Klärungspunkten, E-Mail-Benachrichtigung aus. Kein Multistage, kein Human-review-Connector. Ausgang `outcome`; Kommentar, Prüfer und Zeitpunkt aus `responses[0].comments`, `responses[0].responder.email`, `responses[0].responseDate` (auf Microsoft Learn prüfen).
- Kommentar leer oder nur Leerzeichen: nur `kt_technical_status` = `human_validation_failed`, Entscheidung bleibt angefragt. Sonst genau diese Zeile aktualisieren: Entscheidung freigegeben/abgelehnt, Kommentar unverändert, Prüfer, Zeitpunkt, `kt_technical_status` = `human_decided`. Technische Fehler nach der Antwort: `technical_failed` an derselben Zeile, nie eine Genehmigung vortäuschen.

## 3. Agent Flow „Freigabestatus abrufen <Vorname>“

- Texteingaben: die sechs Bindungswerte und `approval_row_id`. Genau diese Zeile lesen, nie „die jüngste Zeile zu review_id“.
- Alle sechs Bindungsfelder gegen die Zeile prüfen. Bei Lesefehler oder Abweichung: entscheidung `Bindung abgewiesen`, übrige Ausgaben leer.
- „Respond to the agent“ mit fünf Textausgaben: `entscheidung`, `kommentar`, `pruefer`, `zeitpunkt`, `technical_status`. freigegeben/abgelehnt nur bei `human_decided` und passendem Choice-Wert, sonst angefragt. Alle Ausgaben müssen echte Strings sein, auch vor der Entscheidung: nullable Spalten mit `coalesce(..., '')` absichern.

## 4. Topic „Freigabestatus abrufen“

- Abweisen bei fehlender oder fremder Laufbindung oder fehlender `Global.approval_row_id`.
- Status-Flow aufrufen, dann Entscheidung, Kommentar, Prüfer, Zeitpunkt, Technik, run_id und response_id anzeigen. Danach alle Dialoge beenden.

## 5. Tools und Routing

- Für jeden neuen Flow ein TaskDialog-Wrapper unter `actions/` (InvokeFlowTaskAction), Name mit Zusatz „<Vorname>“, also anders als die Topics. „Only when referenced by topics or agents“ wie beim Rückruf-Beispiel. Keine doppelten Registrierungen, keine zwei Namen, die denselben normalisierten Tool-Identifier ergeben. Ersetzte eigene Wrapper entfernen.
- In `agent.mcs.yml` die Instructions um diese Zeile ergänzen: „Klärungspunkte des gespeicherten Laufs gehen nur an [Klärungspunkte freigeben], menschlicher Freigabestatus nur an [Freigabestatus abrufen]. Nicht als neue Prüfung behandeln.“ Die beiden Namen als native Topic-Referenz im Format `{System.Bot.Components.Topics.'<Schemaname>.topic.<TopicSchema>'.DisplayName}` einsetzen. Gelingt das nicht, in `UE16-README.md` ausdrücklich sagen, dass ich die Namen in Copilot Studio per `/` verlinken muss.

## Prüfkriterien aus früheren Fehlern

- Alle acht neuen Dateien wirklich anlegen: zwei `workflow.json`, zwei `metadata.yml` (`jsonFileName` auf den neuen Pfad), zwei Wrapper, zwei Topics.
- `runAfter` nur auf Aktionen derselben Ebene; keine Scope-Grenzen überqueren. Formeln auf Klammern und Syntax prüfen.
- Foundry `output[]` und `content[]` sind Arrays. Filter getrennt von Select, kein `where` in Select.
- Jeder Fehlerpfad vor der Antwort antwortet mit demselben Ausgabeschema; nie erfundener Erfolg.
- Topic-Variablen korrekt deklarieren und binden; flache skalare Flow-Ausgaben statt nicht deklarierter Record-Felder. YAML im nativen Format, keine expliziten null-Werte.
- Ein akzeptierter Push beweist nichts: die eigenen Flow-Datensätze zurücklesen (`clientdata`) und mit der lokalen Definition vergleichen, dann aktivieren und `TemplateValidationError` selbst beheben. Ändert ein Push eine Definition nicht, mit neuer UUID ersetzen und den alten Wrapper entfernen.
- Beide neuen Flows meiner Solution hinzufügen; push ordnet sie sonst nur der Default Solution zu.

## Formathinweise (aus erprobten Läufen, unbedingt einhalten)

**Flows (`workflow.json`)**
- Trigger: `"type": "Request", "kind": "Skills"`, im Schema die Schlüssel `text`, `text_1`, `text_2`, … in der Reihenfolge der Eingaben; der fachliche Name steht nur in `title`, dazu `"x-ms-content-hint": "TEXT"` und `"x-ms-dynamically-added": true`. Im Flow liest du sie mit `triggerBody()?['text_1']` usw.
- Antwort: `"type": "Response", "kind": "Skills"`, Schema-Schlüssel = fachliche Ausgabenamen (`status`, `approval_row_id`, `entscheidung` …), alle `"type": "string"`, `statusCode` 200. Jede Antwort im selben Flow hat dasselbe Schema.
- `connectionReferences` im Flow: Schlüssel `shared_commondataserviceforapps` und `shared_approvals`, je `api.name` gleich dem Schlüssel, `connection.connectionReferenceLogicalName` = mein logischer Name, `runtimeSource: "embedded"`.
- Dataverse (`type: OpenApiConnection`, `host.apiId` und `connectionName` wie im Rückruf-Beispiel): Zeile anlegen `operationId: CreateRecord` mit `entityName: kt_freigaben` und Parametern `item/<spalte>`; ändern `UpdateRecord` mit `recordId`; lesen `GetItem` mit `recordId`. Die neue ID steht in `outputs('<Aktion>')?['body/kt_freigabeid']`.
- Freigabe: `type: OpenApiConnectionWebhook`, `operationId: StartAndWaitForAnApproval`, Connector `shared_approvals`, Parameter `approvalType: Basic`, `WebhookApprovalCreationInput/title`, `…/assignedTo`, `…/details`, `…/enableNotifications: false`. Ergebnis: `body/outcome` (`Approve`/`Reject`), `body/responses[0]['comments']`, `…['responder']['email']`, `…['responseDate']`.
- Choice-Werte als Zahl schreiben, z. B. `@if(equals(outputs('…')?['body/outcome'],'Approve'),582100001,582100002)`.
- `runAfter` nur auf Aktionen derselben Ebene; Aktionen in einem `If`-Zweig hängen nicht per `runAfter` an Aktionen außerhalb.

**Topics und Tools (`*.mcs.yml`)**
- Übernimm die YAML-Struktur der vorhandenen Prüf-Topics. Power-Fx-Werte (`value: =…`, `condition: =…`) stehen vollständig auf einer Zeile, bei Sonderzeichen in Anführungszeichen. Keine gefalteten Blöcke (`>-`, `|`) für Formeln.
- Nachrichten mit Werten als Text mit Platzhaltern schreiben, z. B. `activity: "Freigabe: {Topic.approvalStatus}. Zeilen-ID: {Topic.approvalRowId}"`, nicht als `="…" & …`-Formel.
- Leerprüfungen als `Len(Trim(Coalesce(Topic.x, ""))) = 0`, nicht `IsBlank(Trim(…))`.
- Flow-Aufruf im Topic: `kind: InvokeFlowAction`, `flowId`, `input.binding` mit den Trigger-Schlüsseln (`text: =Global.review_id`, `text_1: =Global.run_id`, …), `output.binding` mit den Antwort-Schlüsseln (`status: Topic.approvalStatus`), `connectionProperties.mode: Invoker`.
- Fragen: `kind: Question`, `alwaysPrompt: true`, `interruptionPolicy.allowInterruption: false`, `entity: StringPrebuiltEntity`.
- Tool-Wrapper unter `actions/`: `kind: TaskDialog`, `action.kind: InvokeFlowTaskAction` mit derselben `flowId`, `outputs` mit den Antwort-Schlüsseln, wie beim Rückruf-Tool.

**Nach jedem Push zurücklesen**
- Beide Flows: `statecode` 1 und `statuscode` 2, `clientdata` entspricht der lokalen Datei, beide in meiner Solution (Komponententyp 29).
- Beide Topics: die importierten Bedingungen und Werte zurücklesen (Bot-Komponente, Feld `data`) und mit der Datei vergleichen. Ein Push ohne Fehlermeldung und ein leerer Topic checker beweisen nicht, dass das Topic fragt.
- Endet ein Topic im Test ohne die erwartete Frage: den zuletzt ausgeführten Knoten finden, bei Bedarf vorübergehend Meldungen mit Knotennamen und Werten einbauen und vor dem finalen Test wieder entfernen.

## Bekannte Fehlerbilder und ihre Ursache

| Meldung oder Beobachtung | Ursache | Abhilfe |
|---|---|---|
| Flow lässt sich nicht einschalten, `TemplateValidationError` | `runAfter` zeigt über eine `If`-Grenze, oder eine Formel hat eine Klammer zu viel | `runAfter` nur innerhalb derselben Ebene; Formel prüfen; neu pushen, zurücklesen, einschalten |
| `DefinitionRequestMissingFields`, Flow bleibt aus | Trigger- oder Antwortschema nicht im nativen Format | Schema genau wie in den Formathinweisen und im Rückruf-Beispiel |
| Topic checker: fehlende Eingaben, `InvalidBindingInvokeAction` | Topic bindet fachliche Namen statt `text`, `text_1` … | `input.binding` mit Trigger-Schlüsseln, `output.binding` mit Antwort-Schlüsseln |
| Topic endet sofort („Completed“), keine Frage nach dem Prüfer; der Dispatcher meldet trotzdem Erfolg | ein Knoten vor der Frage bricht ab (z. B. leere Formel nach dem Import) oder das Routing landet nicht im Topic | importierte Bot-Komponente zurücklesen, Bedingungen und Werte vergleichen, notfalls vorübergehende Diagnose-Nachrichten |
| Bedingung wurde zu `IsBlank()` ohne Argument | `IsBlank(Trim(…))` übersteht den Import nicht | `Len(Trim(Coalesce(…, ""))) = 0` |
| Nachricht zeigt `="…" & …` wörtlich | Nachricht als Formel geschrieben | Text mit `{Topic.x}`-Platzhaltern |
| „Nein“ startet trotzdem die Freigabe | `BooleanPrebuiltEntity` erkennt deutsches „Nein“ nicht zuverlässig | Antwort als Text, Trim/Lower, ausdrücklich auf „ja“ und „nein“ verzweigen |
| Testchat: `ToolIdentifierConflict` | zwei Tools zeigen auf gleichnamige Flows oder ein alter Wrapper ist noch da | alten Wrapper löschen, Namen eindeutig mit Zusatz <Vorname> |
| Status zeigt `null`-Fehler vor der Entscheidung | Dataverse liefert leere Spalten als `null` | alle Ausgaben mit `coalesce(..., '')` |
| Push meldet Erfolg, Flow verhält sich wie vorher | Definition wurde nicht übernommen | `clientdata` zurücklesen; wenn alt: neue UUID, alte Version wie unter „Grenzen“ entfernen |
| Neue Flows nur in der Default Solution | push ordnet nicht der Solution zu | `pac solution add-solution-component` mit Komponententyp 29 |

## Abnahme, bevor du dich meldest

Prüfe selbst und schreibe das Ergebnis in `UE16-README.md`:

1. Beide neuen Flows: `statecode` 1, `statuscode` 2, `clientdata` gleich der lokalen Datei, Mitglied meiner Solution.
2. Keine ersetzten eigenen Flow-Versionen mehr vorhanden, oder du nennst sie mit ID.
3. Genau zwei neue Tool-Wrapper mit Zusatz <Vorname>, `flowId` = aktive Flow-ID; kein doppelter Wrapper.
4. Beide Topics zurückgelesen: Frage nach Prüfer, Ja/Nein als Text, Flow-Aufruf mit `text`-Schlüsseln, Erfolgsnachricht mit Zeilen-ID, Status mit fünf Werten.
5. Instructions enthalten die Routing-Zeile mit nativen Topic-Verweisen.
6. Was ich noch tun muss: Copilot Studio mit F5 neu laden, Tools und Topic checker ansehen, Testchat, Publish.

## Abgabe

Schreibe `UE16-README.md` in den Workspace: erzeugte Dateien, Flow-IDs, deine Befehle mit echten Ergebnissen, was ich noch in Copilot Studio tun muss. Sag mir dann, dass ich Copilot Studio neu laden, die zwei Tools prüfen und testen kann. Erfinde keinen UI-Test. Wenn ich dir Fehler aus dem Topic checker oder dem Testchat schicke: Ursache in den Dateien suchen, beheben, pushen, zurücklesen, aktivieren und mir sagen, wann ich neu laden soll.
