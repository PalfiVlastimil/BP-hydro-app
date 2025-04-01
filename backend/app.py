"""FLASK REST API"""
import os
import io
import sys
import random
from datetime import datetime, timezone, timedelta
import pytz

from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient, InsertOne
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_bcrypt import Bcrypt
import gridfs
import base64
from PIL import Image

#import all sensors
#importing classes
sys.path.append('sensors/grove')
sys.path.append('sensors/other')
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
tds_sensor = GroveTDS(GROVE_I2C_GPIO_0_PIN)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = "super_secret_key" 
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)

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

user_timezone = pytz.timezone("Europe/Prague")
#Start Mongo client
client = MongoClient(MONGO_URI)
db = client["sensor_database"]
fs = gridfs.GridFS(db)

#collections
sensors = db["sensors"]#sensors
images = db["images"]
user_collection = db["users"]

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

@app.route("/capture_image", methods=["POST"])
@jwt_required()
def capture_image():
    """Capture an image from PiCamera2 and store it in MongoDB"""
    picam2.start()
    image = picam2.capture_array()
    picam2.stop()

    # Convert image to bytes
    image_bytes = io.BytesIO()
    Image.fromarray(image).save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    # Store image in MongoDB
    filename = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + ".jpg"
    file_id = fs.put(image_bytes.read(), filename=filename)

    return jsonify({"message": "Image captured and stored", "file_id": str(file_id)}), 201


@app.route("/latest_image", methods=["GET"])
@jwt_required()
def get_latest_image():
    """Retrieve the most recent image from MongoDB"""
    try:
        latest_file = db.fs.files.find_one(sort=[("uploadDate", -1)])
        if not latest_file:
            return jsonify({"error": "No images found"}), 404

        # Extract metadata
        filename = latest_file.get("filename")
        upload_date = latest_file.get("uploadDate")
        file_size = latest_file.get("length")

        file_id = latest_file["_id"]
        file_data = fs.get(file_id).read()

        # Encode the image data to base64
        encoded_image = base64.b64encode(file_data).decode("utf-8")

        response_data = {
            "filename": filename,
            "upload_date": upload_date.isoformat() if upload_date else None,
            "file_size": file_size,
            "data": encoded_image,
        }

        # Send back the base64 data in JSON
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    #users = users; # Zde bude call na login informace
    #if users and bcrypt.check_password_hash(users.get(password), password):
    if users.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify({'message': 'Login Success', 'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@app.route('/get_recent_data', methods=['GET'])
@jwt_required()
def get_data():
    pipeline = [
        {
            "$sort":  {"report.timestamp": -1}  # Sort by timestamp in descending order to get the most recent records first
        },
        {
            "$group": {
                "_id": "$sensor_id",  # Group by sensor_id
                "sensor_id": {"$first": "$sensor_id"},  # Take the first (most recent) sensor_id
                "report": {"$first": "$report"}
            }
        },
        {
            "$project": {
                "_id": 0,  # Remove the _id field from the result
                "sensor_id": 1,
                "report": 1
            }
        }
    ]
    # Retrive from the database
    result = list(sensors.aggregate(pipeline))
    return jsonify(({"message": "Data retrived successfully", "sensors": result})), 200


@app.route('/save_sensor_data', methods=['POST'])
@jwt_required()
def add_data():
    humid, temp = dht22_sensor.read_dht_data()
    tds_ppm_data = tds_sensor.read_tds_data()
    water_lvl_percentage = water_level_sensor.read_water_level_percentage()
    water_temp = ds18b20_water_temp.read_celsius_data()
    ph_value = ph_meter.read_PH_data(water_temp)
    ec_value = tds_sensor.calculate_EC()
    VPD = dht22_sensor.calculate_VPD()
    liters_per_min = water_flow_meter.read_flow_sensor()
    print(client)
    sensor_readings = [
        {
            "sensor_id": "water_temp_sensor",
            "report": {
                "timestamp": datetime.now(tz=pytz.utc),
                "value": water_temp,
                "unit": "°C",
            },
        },
        {
            "sensor_id": "ph_sensor",
            "report": {
                "timestamp": datetime.now(tz=pytz.utc),
                "value": ph_value,
                "unit": "pH",
            }
        },
        {
            "sensor_id": "ec_sensor",
            "report": {
                "timestamp": datetime.now(tz=pytz.utc),
                "value": ec_value,
                "unit": "mS/cm",
            },
        },
        {
            "sensor_id": "tds_sensor",
            "report": {
                "timestamp": datetime.now(tz=pytz.utc),
                "value": tds_ppm_data,
                "unit": "ppm",
            }
        },
        {
            "sensor_id": "water_level_sensor",
            "report": {
                "timestamp": datetime.now(tz=pytz.utc),
                "value": water_lvl_percentage,
                "unit": "%",
            }
        },
        {
            "sensor_id": "water_flow_sensor",
            "report": {
                "timestamp": datetime.now(tz=pytz.utc),
                "value": liters_per_min,
                "unit": "l/min",
            }
        },
        {
            "sensor_id": "air_temp_sensor",
            "report":{
                "timestamp": datetime.now(tz=pytz.utc),
                "value": temp,
                "unit": "°C",
            }
        },
        {
            "sensor_id": "humidity_sensor",
            "report":{
                "timestamp": datetime.now(tz=pytz.utc),
                "value": humid,
                "unit": "%",
            }
        },
        {
            "sensor_id": "vpd_sensor",
            "report":{
                "timestamp": datetime.now(tz=pytz.utc),
                "value": VPD,
                "unit": "Pa",
            }
        },
    ]
    #Add to database
    sensors.insert_many(sensor_readings)
    return jsonify({"message": "Data added successfully", "inserted_count": len(sensor_readings)}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)