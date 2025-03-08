from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
import sys
sys.path.append('sensors/grove')
sys.path.append('sensors/other')

#This is a rest api
#import all sensors
#importing classes 
from grove_dht22 import DHT22
from grove_servo import GroveServo
from grove_water_level_sensor import GroveWaterLevelSensor
from grove_tds import GroveTDS
#importing modules
import ds18b20_water_temp
import ph_meter
import water_flow_meter
from picamera2 import Picamera2, Preview

# Pins
# Grove AD convertor pin
GROVE_ADC_IN_0 = 0;
# GPIO pins
GROVE_GPIO_12_PIN    = 12
GROVE_GPIO_26_PIN    = 26
GROVE_I2C_GPIO_0_PIN = 0
GROVE_I2C_GPIO_1_PIN = 1

# Instantiate/Load Grove sensors for data transfer when needed ()
dht22_sensor = DHT22(GROVE_GPIO_12_PIN)
water_level_sensor = GroveWaterLevelSensor(GROVE_I2C_GPIO_1_PIN)
tds_sensor = GroveTDS(GROVE_ADC_IN_0)

app = Flask(__name__)
CORS(app)
# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client.hello_database
collection = db.hello_collection


@app.route('/get_data', methods=['GET'])
def get_data():
    # Simulate reading data from a sensor
    humi, temp = dht22_sensor.read_dht_data()
    data = {
        "humidity": temp or round(random.uniform(40.0, 60.0), 2),
        "temperature": humi or round(random.uniform(20.0, 30.0), 2)
    }
    json_data = jsonify(data)
    return jsonify(json_data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, )