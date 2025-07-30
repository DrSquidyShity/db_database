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

## Schema der Datenbank

Mithilfe des Skripts werden zwei Tabellen erzeugt, die nach folgendem Schema definiert sind:
```
train_data : {[__timestamp__, connection, service_level, gps_status, latitude, longitude, speed, internet, connection_current_state, connection_next_state, connection_remaining_time_seconds, server_time, date, train_number]}
```

```
train : {[__date__, __train_number__, train_type, series, tzn, bap_installed]}
```

## Mock-API

Zum Testen bzw. Anpassen des Skripts, wird eine einfache Mock-API bereitgestellt.
Diese kann vor allem dann hergenommen werden, falls man nicht im Zug sitzt.
Diese lässt sich folgendermaßen aufsetzen:
```
cd mock-api
docker build -t mock-ice-api .
docker run --rm -p 5001:5000 mock-ice-api
```
Gerne natürlich auch auf einem anderen Hostport (*hier: 5001*) ausführen.
Dieser muss entsprechend im Skript in der globalen Variable oben angepasst werden.

Damit die echte Datenbasis nicht versehentlich verändert wird, wird an den oben angegebenen Dateinamen vorher *test_* angehängt. Das funktioniert automatisch, indem wir die "-t" flag zu unserem Programmaufruf hinzufügen, ansonsten funktioniert alles wie zuvor.
