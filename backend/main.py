import time
import os
import traceback
import sys
sys.path.append('backend/sensors/grove')
sys.path.append('backend/sensors/other')

#importing classes from modules
from grove_dht22 import DHT22
from grove_servo import GroveServo
from grove_water_level_sensor import GroveWaterLevelSensor
from grove_tds import GroveTDS

#importing modules
import ds18b20_water_temp
import ph_meter
import water_flow_meter
from picamera2 import Picamera2, Preview

# Grove AD convertor pin
GROVE_ADC_IN_0 = 0;
# pins
GROVE_GPIO_12_PIN    = 12
GROVE_GPIO_26_PIN    = 26
GROVE_I2C_GPIO_0_PIN = 0
GROVE_I2C_GPIO_1_PIN = 1
picam2 = Picamera2()
app_is_running = True

def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If computer is running windows use cls
        command = 'cls'
    os.system(command)

def switch_menu(number):
  if number == 1:
    dht22_sensor = DHT22(GROVE_GPIO_12_PIN)
    print(dht22_sensor.read_dht_data())
  elif number == 2:
    servo = GroveServo(GROVE_GPIO_26_PIN)
    servo.sweep(True)
  elif number == 3:
    water_level_sensor = GroveWaterLevelSensor(GROVE_I2C_GPIO_1_PIN)
    print(water_level_sensor.read_water_level_percentage())
    #water_level_sensor.loop_sensor(True)
  elif number == 4:
    sensor = GroveTDS(GROVE_I2C_GPIO_0_PIN)
    sensor.loop_sensor()
  elif number == 5:
    #ds18b20_water_temp.loop_sensor()
    print(ds18b20_water_temp.read_celsius_data())
  elif number == 6:
    dht22_sensor = DHT22(GROVE_GPIO_12_PIN)
    humid, temp = dht22_sensor.read_dht_data()
    #PH = ph_meter.read_PH_data(temp)
    #print("PH: ", PH)
  elif number == 7:
    while True:
      try:
        tds_sensor = GroveTDS(GROVE_I2C_GPIO_0_PIN)
        EC = tds_sensor.calculateEC()
        time.sleep(2)
        print(EC)
      except KeyboardInterrupt:
        break
      except Exception as e:
        print("Error on EC calculation: ", e)
        break
  elif number == 8:
    #water_flow_meter.loop_sensor()
    water_flow_meter.read_sensor_liters()
  elif number == 9:
    global picam2
    timestr = time.strftime("%d%m%y-%H%M%S")
    picam2.start_and_record_video(timestr + ".mp4", duration=5)
  else:
    print("Nevalidní vstup. Zkuste to ještě jednou.")
    return

def main():
  global app_is_running
  print("Vítej v testoavací aplikaci")
  #Initialize all sensors
  while app_is_running:
    print("Vyber si senzor:")    
    print("01. Grove - DHT22 senzor                (Funguje)")    
    print("02. Grove - Servo                       (Funguje)")    
    print("03. Grove - Senzor vodní hladiny        (Funguje)")    
    print("04. Grove - TDS senzor                  (Funguje)")    
    print("05. Other - Vodní senzor DS18B20        (Funguje)")    
    print("06. Other - PH metr                     (Funguje)")    
    print("07. Other - EC výpočet                  (Funguje)")
    print("08. Other - Senzor vodního toku         (Funguje)")
    print("09. Preview kamerky                     (Funguje)")
    print("10. Ukončit program")
    try:
      number_input = int(input("Vyber si z těchto možností [1-9]:"))
      switch_menu(number_input)
      if number_input == 9:
        app_is_running = False
        break
    except Exception as error:
      print("Error zpráva:", error)
      traceback.print_exc()
  print("Ukončuje se program…")
if __name__ == "__main__":
  main()
