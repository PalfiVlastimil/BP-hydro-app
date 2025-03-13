from flask import Flask, jsonify
from pymongo import MongoClient, InsertOne
from flask_cors import CORS
import os
import sys
import random
import datetime
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
#import ph_meter
import water_flow_meter
#from picamera2 import Picamera2, Preview Why this doesnt work????

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
#app.config
# Connect to MongoDB
PORT = os.environ.get("PORT")
DB_User = os.environ.get("DB_User")
DB_Password = os.environ.get("DB_Password")
DB_Host = os.environ.get("DB_Host")
DB_Port = os.environ.get("DB_Port")
MONGO_URI = os.getenv("MONGO_URI", f"mongodb://{DB_User}:{DB_Password}@{DB_Host}:{DB_Port}/test_database?authSource=admin")
#"hydro-mongo", 27017, username="admin", password=os.getenv("DB_Password")
client = MongoClient(MONGO_URI)
db = client["test_database"]
print(db.list_collection_names())
sensors = db["test_collection"]#sensors


@app.route('/get_dht', methods=['GET'])
def get_data():
    # Simulate reading data from a sensor
    humi, temp = dht22_sensor.read_dht_data()
    data = {
        "humidity": humi or None,
        "temperature": temp or None
    }
    json_data = jsonify(data)
    return json_data
# TODO Plan out, how should database work, and what CRUD operations will be here
@app.route('/data', methods=['POST'])
def add_data():
    humi, temp = dht22_sensor.read_dht_data()
    water_lvl_percentage = water_level_sensor.read_water_level_percentage()
    #tds_ppm_data = tds_sensor.read_tds_data()
    print(client)
    sensor_readings = [
        {
            "sensor_id": "DHT22_sensor",
            "timestamp": datetime.datetime.now(),
            "temp": temp,
            "humi": humi,
            "unit": "°C, %",
        },
        {
            "sensor_id": "grove_water-level_sensor",
            "timestamp": datetime.datetime.now(),
            "value": water_lvl_percentage,
            "unit": "%",
        },
    ]
    #add to database
    sensors.insert_many(sensor_readings)
    return jsonify({"message": "Data added successfully", "inserted_count": len(sensor_readings)}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)