import sys
import traceback
sys.path.append('backend/lib/DFRobot')
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


def print_sensor_data(ambient_temperature, analog_pin):
  #set IIC address
  ads1115.setAddr_ADS1115(0x48)
  #Get the Digital Value of Analog of selected channel
  adc0 = ads1115.readVoltage(analog_pin) #0
  print("A0:%dmV "%(adc0['r']))
  #Calibrate the calibration data
  ph.calibration(adc0['r'])
  PH = ph.read_PH(adc0['r'], ambient_temperature)
  ph.reset()

def read_PH_data(ambient_temperature, analog_pin):
  try:
    
    # Set IIC address
    ads1115.setAddr_ADS1115(0x48)
    # Calibrate the voltage before reding it 
    ads1115.setGain(ADS1115_REG_CONFIG_PGA_1_024V)
    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.readVoltage(analog_pin) #0
    print("A0:%dmV "%(adc0['r']))
    #Calibrate the calibration data
    ph.calibration(adc0['r'])
    PH = ph.read_PH(adc0['r'], ambient_temperature)
    ph.reset()
    return PH
  except Exception as e:
    print(f"Error reading from sensor: {e}")
    print(traceback.format_exc())
    return None
    
