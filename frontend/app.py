from flask import Flask
import requests

app = Flask(__name__)

BACKEND_URL = 'http://hydro-backend:5000/get_data'

@app.route('/')
def index():
    response = requests.get(BACKEND_URL)
    data = response.json()
    return f"<h1>{data['humidity']} and {data['temperature']}°C</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)