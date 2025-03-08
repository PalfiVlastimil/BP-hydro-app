from flask import Flask
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:5000/api/hello"

@app.route('/')
def index():
    response = requests.get(BACKEND_URL)
    data = response.json()
    return f"<h1>{data['message']}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)