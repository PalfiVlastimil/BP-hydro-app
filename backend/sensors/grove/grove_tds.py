import math
import sys
import time
import pytz
from grove.adc import ADC

class GroveTDS:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def tds(self):
        value = self.adc.read(self.channel)
        if value != 0:
            voltage = value*5/1024.0
            tdsValue = (133.42*voltage*voltage*voltage-255.86*voltage*voltage+857.39*voltage)*0.5
            return tdsValue
        else:
            return 0
    def loop_sensor(self):
        print('Detecting TDS...')
        while True:
            try:
                print('TDS Value: {0}'.format(self.tds))
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def read_tds_data(self):
        print('Detecting TDS...')
        return self.tds
    def calculateEC(self, k_factor_type  = 0):
        """
            calculates EC value based on TDS value
            ppm_value: value of TDS
            k_factor_type: TDS conversion factor, a constant, which approximates EC value based on the type of water
                - choose between [0: pure water (default), 1: groundwater, 2: seawater]
            returns: EC value in  microsiemens per centimeter (μS/cm)
        """
        if k_factor_type > 2 or k_factor_type < 0:
            return
        k_factor = [700,650,500]
        result = self.tds/k_factor[k_factor_type]
        return result