# DB API Database (für im Zug)

Kleines Projekt, um Anfragen an die API der Deutschen Bahn zu stellen.

Easy Setup in einer virtuellen Umgebung:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Um mit dem Programm die Zugdaten einer Fahrt aufzunehmen, mit dem Zug-WiFi verbinden und folgenden Befehl ausführen:
```
python3 track_train.py <ICE_NUMMER>
Eg. python3 track_train.py 42
````

Um sich die Datenbasis anzuschauen, kann folgender Befehl verwendet werden:
```
python3 track_train.py -d
```


## Mock API

Zum Testen bzw. Anpassen des Skripts, wird eine einfache MockAPI bereitgestellt.
Diese kann vor allem dann hergenommen werden, falls man nicht im Zug sitzt.
Diese lässt sich folgendermaßen aufsetzen:
```
cd mock-api
docker build -t mock-ice-api .
docker run -p 5001:5000 mock-ice-api
```
Gerne natürlich auch auf einem anderen Hostport ausführen.
Entsprechend die `URL` Variable im Skript `track_train-py`anpassen.