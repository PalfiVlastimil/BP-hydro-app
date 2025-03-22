"""FLASK REST API"""
from flask import Flask, request, jsonify
from pymongo import MongoClient, InsertOne
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_bcrypt import Bcrypt
import os
import sys
import random
import datetime
import pytz
sys.path.append('sensors/grove')
sys.path.append('sensors/other')


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
tds_sensor = GroveTDS(GROVE_I2C_GPIO_0_PIN)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = "super_secret_key" 
app.config['JWT_TOKEN_LOCATION'] = ['headers']

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)
users = {"admin": "password123"}

#app.config
# Connect to MongoDB
PORT = os.environ.get("PORT") or 8081
DB_User = os.environ.get("DB_User") or "admin"
DB_Password = os.environ.get("DB_Password") or "password"
DB_Host = os.environ.get("DB_Host") or "localhost"
DB_Port = os.environ.get("DB_Port") or "50002"
MONGO_URI = os.getenv("MONGO_URI", f"mongodb://{DB_User}:{DB_Password}@{DB_Host}:{DB_Port}/sensor_database?authSource=admin")


client = MongoClient(MONGO_URI)
db = client["sensor_database"]
user_timezone = pytz.timezone("Europe/Prague")
sensors = db["sensors"]#sensors
user_collection = db["users"]

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    #users = users; # Zde bude call na login informace
    #if users and bcrypt.check_password_hash(users.get(password), password):
    if users.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
@app.route('/sensors/{id}', methods=['GET'])
def get_sensor_data():
    pass
# TODO Plan out, how should database work, and what CRUD operations will be here
@app.route('/save_sensor_data', methods=['POST'])
#@jwt_required()
def add_data():
    humid, temp = dht22_sensor.read_dht_data()
    tds_ppm_data = tds_sensor.read_tds_data()
    water_lvl_percentage = water_level_sensor.read_water_level_percentage()
    water_temp = ds18b20_water_temp.read_celsius_data()
    ph_value = ph_meter.read_PH_data(water_temp)
    ec_value = tds_sensor.calculateEC()
    VPD = dht22_sensor.calculate_VPD()
    liters_per_min = water_flow_meter.read_flow_sensor()
    
    print(client)
    sensor_readings = [
        {
            "sensor_id": "ds18b20_water_temp",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": water_temp,
            "unit": "°C",
        },
        {
            "sensor_id": "ph_meter",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": ph_value,
            "unit": "pH",
        },
        {
            "sensor_id": "ec",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": ec_value,
            "unit": "μS/cm",
        },
        {
            "sensor_id": "grove_tds",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": tds_ppm_data,
            "unit": "ppm",
        },
        {
            "sensor_id": "grove_water-level_sensor",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": water_lvl_percentage,
            "unit": "%",
        },
        {
            "sensor_id": "water_flow_meter",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": liters_per_min,
            "unit": "l/min",
        },
        {
            "sensor_id": "DHT22_sensor",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "temp": temp,
            "humi": humid,
            "unit": "°C, %",
        },
        {
            "sensor_id": "water_pressure_deficit",
            "timestamp": datetime.datetime.now(tz=pytz.utc),
            "value": VPD,
            "unit": "Pa",
        },
    ]
    
    #add to database
    sensors.insert_many(sensor_readings)
    return jsonify({"message": "Data added successfully", "inserted_count": len(sensor_readings)}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)