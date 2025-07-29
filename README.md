# DB API Database

Kleines Projekt, um anfragen die API der deutschen Bahn zu stellen.

Easy Setup in einer virtuellen Umgebung für das DB Skript:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Zum Testen und Abändern falls man nicht im Zug sitzt, gibt es die Mock-API:
```
cd mock-api
docker build -t mock-ice-api .
docker run -p 5001:5000 mock-ice-api
```
Gerne natürlich auch auf einem anderen Hostport ausführen.
Entsprechend die `URL` Variable im Skript `track_train-py`anpassen.