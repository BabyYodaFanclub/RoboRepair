# DeliverBot Feedback

## General
- [ ] Speichern von States
  - Dict mit username/chat_id -> (current_level, global_state)
  - save everytime user go to next level / every n minutes (if changes)
- [ ] Achivements
  - Sammeln von Tieren
  - Mindestens n Robotern helfen  

### Actions
- [ ] Leerzeilen überspringen / Kommentar-zeilen mit `#`
- [ ] Rename Actions, Dokumentieren
- [ ] Syntax überarbeiten, damit regex für Keywords verwendet werden können
- [ ] `.location` Datei, pro Level (oder mit set location), um collectables und bestimmte fragen auf einen Ort festzusetzten
- [ ] Neue Aktion: `Set var`
  - `[Set=varname] value`
- [ ] Neue Aktion: `Collect` (Nur für eine .location Datei)
  - `[Collect=keyword] Text`
- [ ] Neue Aktion: `Diverse`
  - `[Diverse=n]` die nächsten wähle einen der nächsten `n` Einträge (nur `i`) und mache dann nach diesen weiter
- [ ] Neue Aktion: `Select` mit `Options`
  - `[Select=n] Question` sagt: die nächsten `n` einträge sind Options
  - `[Option=linenumber,keyword,keyword]` sagt: wenn eins der Keywords getroffen wurde springe in Zeile
- [ ] Neue Aktion: `Jump`, kann `c` ersetzen (damit wüden dann auch alle antworten in variablen gespeichert)
  - `[Jump=varname,linenumber,linenumber]`
  
## Input  
- [ ] Regex für Antworten
  - z.B.: für 'take leg', 'take your leg' -> 'take[\w\s]*leg'
- [ ] Tipps nach n Falscheingaben
- [ ] Generelle Antworten (unabhängig vom Level)
  - vielleicht als ordner mit generellen Fragen / Antworten (.dialog-files) 
  - Send a update / Send a image
  - Wie gehts
- [ ] Hilfestellungen für Antworten (help)
  - z.B.: beim image sensor -> 'es ist viel zu hell'

#### needs to be done
+ zu viel Raten  mit Phrasen, mehr Variety erlauben
+ sollte auch auf random Eingaben reagieren können
  + Wie gehts? - **in der Story:** gerade etwas ängstlich, nicht so gut; **nach der Story:** sehr gut, ich hab Spaß, es macht Spaß die Galaxie zu erkunden
  + nice/ cool - ja, nicht wahr?
  + was? - wiederholt letzten Satz -- den letzten satz kann man doch lesen?
  + schick ein Update - schickt letztes Bild
  + Hilfe - gibt Hinweise  
#### wishful thinking


## Writing
+ help I'm melting I want to be friends with him forever he's too cute
#### needs to be done
- [x] sollte immer mal wieder random Updates schicken
  - solange der User das Spiel nicht abgeschlossen hat, bekommt er Täglich eine Message
- [x] sollte nach Beendung des Spiels noch ansprechbar sein mit random Phrasen (siehe oben)
  - Nach beendigung des Spiels sendet er eine Nachricht das er angekommen ist, wenn man ihn dann anspricht sagt er, das man auch anderen Robotern helfen kann indem man /start eingibt
#### wishful thinking
+ cool wäre es, wenn er nach dem Spiel "zu was nütze wäre", e.g. advice, helping with planning oder so

## Graphics
- needs to be done 
  - [ ] Ein Bild wie er glücklich angekommen ist (Selfie), damit das letzte Bild nicht ist, wie er sich selbst schweißt
- wishful thinking
  - [ ] super cool wären 4/ 5 Bilder von ihm an in verschiedenen Orten, die er zu den random Updates schickt
  - [ ] mit den Bildern könnte man ein Narrative bauen, was z.B. auch auf Instagram gepostet werden könnte (gleichzeitig auch ne Promotion für den Bot)

## Website
- [ ] Domain / Github-page
- [ ] Styling (konsistent mit Logo + Spiel)
- [ ] Homepage
- [ ] Verlinkung aus dem Menu zu den einzelnen Robotern und zu General Troubleshooting
- [ ] (Seperate Seiten)
  - [ ] Pro Roboter
  - [ ] General Troubleshooting
  - [ ] About us / Contact / Legal als 
