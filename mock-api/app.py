from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api1/rs/status')
def status(): 
    return jsonify({
        "connection": True,
        "serviceLevel": "AVAILABLE_SERVICE",
        "gpsStatus": "VALID",
        "internet": "HIGH",
        "latitude": 48.40851,
        "longitude": 11.464837,
        "tileY": -177,
        "tileX": 133,
        "series": "407",
        "serverTime": 1753873569920,
        "speed": 88.8,
        "trainType": "ICE",
        "tzn": "ICE4714",
        "wagonClass": "FIRST",
        "connectivity": {
            "currentState": "WEAK",
            "nextState": "UNSTABLE",
            "remainingTimeSeconds": 1800
        },
        "bapInstalled": True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
