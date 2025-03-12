import math
import sys
import time
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