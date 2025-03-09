#!/usr/bin/env python
import os

def get_sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20

def read_sensor_data(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius

def loop(ds18b20):
    while True:
            if read_sensor_data(ds18b20) != None:
                print("Current temperature : %0.3f C" % read_sensor_data(ds18b20))
def read_celsius_data():
    try:
        serialNum = get_sensor();
        celsius = read_sensor_data(serialNum)
        if serialNum is None: return None
        if celsius is None: return None
        return celsius;
    except Exception as e:
        print(f"Error reading from sensor: {e}")
        return None  

def kill():
    quit()
def loop_sensor():
    serialNum = get_sensor()
    loop(serialNum)
if __name__ == '__main__':
    try:
        loop_sensor()
    except KeyboardInterrupt:
        kill()
