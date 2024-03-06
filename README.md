# edi.filetriage  
  
Mit dem Package edi.filetriage können Dateien bzw. Datei-Objekte, Listen von Dateien und Verzeichnisse auf bösartige Inhalte untersucht werden. Es kann z.B. als Upload-Filter verwendet werden. Erkannte potenzielle Risiken sind z.B.:  

- Dateiname stimmt nicht mit dem ermittelten Dateityp (laut Header) überein  
- Datei enthält Aktionen oder Prozeduren, die beim Öffnen von Dateien ausgeführt werden  
- Datei enthält (ggf. bösartige) Skripte, Makros, ...  
- PDF-Datei enthält keine Seiten und Skripte (Hinweis auf bösartigen Code)  

Hinweis: mit diesem Package wird lediglich eine Art Vorselektion und eine große Risikobewertung durchgeführt, es werden keine qualifizierten Belege ermittelt, ob tatsächlich ein Risiko vorliegt oder nicht.  
  
  
## Installation  
  
Falls noch nicht vorhanden, muss libmagic installiert werden:  
  
```  
sudo apt-get install libmagic-dev  
```  
  
Installation mit pip:  
  
```  
pip install filetriage@git+https://github.com/educorvi/edi.filetriage.git  
```  
  
  
## Dokumentation
  
### checker.py - Hauptfunktionalitäten
**analyse_file**(*file_object, check_file_extension=True*)
- Untersucht ein Dateiobjekt auf bösartigen Inhalt
- *file_object*: Das Dateiobjekt (z.B. erzeugt mit open())
- *check_file_extension*: (bool) True, falls die Dateiendung auf Gültigkeit überprüft werden soll
- Rückgabe: dictionary mit folgenden Elementen:
	- `'success': False` falls ein Fehler auftritt (dann `'risk': None`), sonst `'success': True` und `'risk': 0..3`
	- `'risk'`: `0` kein Risiko, `1` niedriges Risiko,  `2` mittleres Risiko, `3` hohes Risiko, `None` im Fehlerfall
	- `'mimetype'`: ermittelter Mimetype der Datei, z.B. `application/pdf`
	- `'result'`: Kurzer String, der das Ergebnis der Prüfung beschreibt (siehe results.py)  
	- `'message'`: Lange, lesbare Beschreibung des Risikos / des Fehlers (siehe results.py)  

**analyse_file_list**(*file_object_list, check_file_extension=True, prints=False, merge_results=True*)
- Untersucht eine Liste von Dateiobjekten auf bösartigen Inhalt
- *file_object_list*: List von Dateiobjekten (z.B. erzeugt mit open())
- *check_file_extension*: (bool) True, falls die Dateiendung auf Gültigkeit überprüft werden sollen
- *prints*: (bool) True, falls der Fortschritt und Meldungen in der Konsole ausgegeben werden sollen
- *merge_results*: (bool) True, falls die Ergebnisse nach Risiko und Meldung gruppiert werden sollen
- Rückgabe: dictionary, das die Ergebnisse gruppiert nach erfolgreichen / nicht erfolgreichen Prüfungen und Risikoleveln enthält, mit folgender Form:
```
{
    "successful": [
        {
            "risk": 0,
            "count": 1,
            "results": [],
        },
        {
            "risk": 1,
            "count": 2,
            "results": [
                {
                    "result": "pdf_action",
                    "message": "...",
                    "count": 1,
                    "files": [
                        {
                            "path": "...",
                            "mimetype": "...",
                        },
                    ],
                },
                {
                    "result": "pdf_script",
                    "message": "...",
                    "count": 1,
                    "files": [
                        {
                            "path": "...",
                            "mimetype": "...f",
                        },
                    ],
                },
            ],
        },
        {
            "risk": 2,
            "count": 0,
            "results": [],
        },
        {
            "risk": 3,
            "count": 0,
            "results": [],
        },
    ],
    "not_successful": [
    	{
        	"result": "unknown_mimetype",
            "message": "...",
            "count": 1,
            "files": [
                {
                    "path": "...",
                    "mimetype": "...f",
                },
            ],
        },
    ],
}
```

**analyse_directory**(*absolute_path, recursive=True, check_file_extension=True, prints=False, merge_results=True*)
- Untersucht alle Dateien in einem Verzeichnis auf bösartigen Inhalt
- *absolute_path*: (str) Absoluter Pfad des Ordners
- *recursive*: (bool) Rekursiv in Unterverzeichnisse absteigen
- *check_file_extension*: (bool) True, falls die Dateiendung auf Gültigkeit überprüft werden sollen
- *prints*: (bool) True, falls der Fortschritt und Meldungen in der Konsole ausgegeben werden sollen
- *merge_results*: (bool) True, falls die Ergebnisse nach Risiko und Meldung gruppiert werden sollen
- Rückgabe: dictionary, gleiche Form wie bei **analyse_file_list**

**check_extension**(*filename, mimetype*)
- Überprüft, ob die Dateiendung gültig für einen gegebenen Mimetype ist
- *filename*: (str) Dateiname oder ganzer Pfad
- *mimetype*: (str) Mimetype der überprüft werden soll
- Rückgabe: (dict) `{'valid': <None / True / False>, 'message': str}` (falls ein Fehler auftritt: `'valid': None`)

### examiner.py
Enthält die Untersuchungsfunktionen der Form **examine_\<type\>**(*file_object, mimetype*). Diese werden in den **analyse_**-Funktionen bei entsprechendem Mimetype aufgerufen. 

### types_helper.py
Im dictionary `methods` können die **examine**-Funktionen den Mimetypes zugeordnet werden. Die Datei enthält außerdem Hilfsfunktionen zur Prüfung des Mimetypes und der Extension.

### results.py
Enthält Fehlermeldungen und Nachrichten zu den Untersuchungsergebnissen mit entsprechender Risiko-Bewertung. Über die zwei Funktionen werden die Dictionaries für die Rückgaben erzeugt.

### file_extensions.py
Enthält alle für jeweils einen Mimetype gültigen Extensions.
