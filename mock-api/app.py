from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/jetty/api/v1/status')
def status():
    return jsonify({
        "connection": True,
        "servicelevel": "SERVICE",
        "speed": 185.8000030517578,
        "longitude": 10.924448,
        "latitude": 52.432009,
        "serverTime": 1445351850874
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
