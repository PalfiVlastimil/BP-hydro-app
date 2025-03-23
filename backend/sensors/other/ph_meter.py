import sys
import traceback
sys.path.append('backend/lib/DFRobot')
sys.path.append('lib/DFRobot')

import time
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16

from DFRobot_ADS1115 import ADS1115
from DFRobot_PH      import DFRobot_PH

ads1115 = ADS1115()
ph      = DFRobot_PH()

def read_PH_data(water_temperature):
  try:
    calibration_value = 5.4
    ph.reset()
    ph.begin()
    # Set IIC address
    ads1115.setAddr_ADS1115(0x48)
    # Get the Digital Value of Analog of selected channel
    ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
    adc0 = ads1115.readVoltage(0)
    #print("A0:%dmV "%(adc0['r']))
    #Calibrate the calibration data
    PH = ph.read_PH(adc0['r'], water_temperature)+calibration_value 
    return PH
  except Exception as e:
    print(f"Error reading from sensor: {e}")
    print(traceback.format_exc())
    return None
  
"""Funkce dole slouží pro kalibraci s main.py, poté se dá využít PH metr při nasazení h"""
def loop_PH_data(water_temperature):
  try:
    calibration_value = 5.4
    ph.begin()
    while True:
      # Set IIC address
      ads1115.setAddr_ADS1115(0x48)
      #Sets the gain and input voltage range.
      ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
      # Get the Digital Value of Analog of selected channel
      adc0 = ads1115.readVoltage(0)
      #Calibrate the calibration data
      PH = ph.read_PH(adc0['r'], water_temperature)+calibration_value
      print ("Temperature:%.1f ^C PH:%.2f" %(water_temperature,PH))
      print("A0 voltage:%dmV "%(adc0['r']))
      time.sleep(1.0)
  except Exception as e:
    print(f"Error reading from sensor: {e}")
    print(traceback.format_exc())

def loop_voltage_calibration():
  try:
    ph.begin()
    while True:
      # Set IIC address
      ads1115.setAddr_ADS1115(0x48)
      # Get the Digital Value of Analog of selected channel
      ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
      adc0 = ads1115.readVoltage(0)
      print("A0:%dmV "%(adc0['r']))
      #Calibrate the calibration data
      ph.calibration(adc0['r'])
      time.sleep(1.0)
  except Exception as e:
    print(f"Error reading from sensor: {e}")
    print(traceback.format_exc())