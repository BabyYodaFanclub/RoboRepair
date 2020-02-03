# DeliverBot Feedback

## General
- [ ] Speichern von States
  - Dict mit username/chat_id -> (current_level, global_state)
  - save everytime user go to next level / every n minutes (if changes)
- [ ] Achivements
  - Sammeln von Tieren (Stickerpack)
  - Mindestens n Robotern helfen  
- [ ] Möglichst viel (vielleicht alle) Logik aus den Level.py dateien in die .dialog Dateien umbauen
  - bzw in eine .level Datei

### Actions
- [ ] Leerzeilen überspringen / Kommentar-zeilen mit `#`
- [ ] Rename Actions, Dokumentieren
- [ ] Syntax überarbeiten, damit regex für Keywords verwendet werden können
- [ ] `.location` Datei, pro Level (oder mit set location), um collectables und bestimmte fragen auf einen Ort festzusetzten
- [ ] Neue Aktion: `send voice`
  - `[send_voice=(file_name)] (Text)`: Entweder von einer Datei, oder mit TextToSpeech
- [ ] Neue Aktion: `set var`
  - `[set_var=varname] value`
- [ ] Neue Aktion: `collect` (Nur für eine location/level.message Datei aber **nicht** für dialog.message)
  - `[collect=keyword] Text`
- [ ] Neue Aktion: `diverse`
  - `[diverse=n]` die nächsten wähle einen der nächsten `n` Einträge (nur `i`) und mache dann nach diesen weiter
- [ ] Neue Aktion: `select` mit `options`
  - `[select=n] Question` sagt: die nächsten `n` einträge sind Options
  - `[option=linenumber,keyword,keyword]` sagt: wenn eins der Keywords getroffen wurde springe in Zeile
- [ ] Neue Aktion: `Jump`, kann `c` ersetzen (damit wüden dann auch alle antworten in variablen gespeichert)
  - `[jump=var_name,linenumber_x,linenumber_y]`: if var_name: x else: y
- [ ] Neue Aktion: `Change Location`
  - `[location=location_name]`: Change the current location to location_name
- [ ] ? Neue Aktion: `Load Dialog`
  - `[dialog=dialog_name]`: Springt in einen Dialog, und "merkt" sich die Rücksprung-addresse (index+1)
  
### Level
- [ ] Level-Struktur anpassen
  - Levels/level_name/.level -> keywords: {(active, variants, function), ...}
  - Levels/level_name/.message
  - Levels/level_name/images/image_name.png
  - Levels/level_name/dialog/dialog_name.message
  
### Locations
- [ ] Definieren von locations (Ordner Locations/location_name/)
- [ ] Definieren von location-file (Order Locations/location_name/location)
- [ ] Definieren von einer location sensitiven .message Datei
- [ ] ?Bilder in Locations/location_name/images/image_name.png
- [ ] ?Audio? in Locations/location_name/audio/audio_name.[mp3/ogg]
- [ ] .achivements (die hier gesammelt werden können) ?

  
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
- [ ] Verschiedene Beschreibungen/Stats für die einzelnen Roboter
