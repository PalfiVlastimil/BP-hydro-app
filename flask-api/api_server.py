from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    # Simulate reading data from a sensor
    data = {
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(40.0, 60.0), 2)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)  # Run on all interfaces, port 5001