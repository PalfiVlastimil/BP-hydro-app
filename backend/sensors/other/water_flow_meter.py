#!/usr/bin/env python
#DEBUG = True
DEBUG = False
import time, sys
import RPi.GPIO as GPIO
from datetime import datetime
GPIO.setmode(GPIO.BCM)
def loop_sensor():
  
  # configurations
  pin_input = int(8)
  #
  GPIO.setup(pin_input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  # variables
  total_liters = 0
  secondes = 0

  # Sampling
  sample_rate = 10  # Sampling each 10 secondes
  time_start = 0
  time_end = 0
  period = 0;
  hz = []       # Frequency !important!
  m = 0.0021    # See linear.pdf

  # data 
  db_good_sample = 0
  db_hz = 0
  db_liter_by_min = 0
  
  print("Water Flow - YF-S201 measurment")

  while True:
    # start / end 
    time_start = time.time()
    init_time_start = time_start # undetect last edge 
    time_end = time_start + sample_rate
    hz = []
    sample_total_time = 0

    # Edge
    current = GPIO.input(pin_input)
    edge = current # Rising edge / Falling edge

    try:
        while time.time() <= time_end:
            t = time.time()
            v = GPIO.input(pin_input)
            if current != v and current == edge:
                period = t - time_start # Impulsion period
                new_hz = 1/period
                hz.append(new_hz)               # Period = 1/period
                sample_total_time += t - time_start
                time_start = t
               
                if DEBUG:
                    print(round(new_hz, 4))     # Print hz
                    sys.stdout.flush()
            current = v

        # Sums
        print('-------------------------------------')
        print('Current Time:',time.asctime(time.localtime()))

        secondes += sample_rate
        nb_samples = len(hz)
        if nb_samples >0:
            average = sum(hz) / float(len(hz))
            # Calcul % of good sample in time range
            good_sample = sample_total_time/sample_rate
            print("\t", round(sample_total_time,4),'(sec) good sample')
            db_good_sample = round(good_sample*100,4)
            print("\t", db_good_sample,'(%) good sample')
            average = average * good_sample
        else:
            average = 0
        average_liters = average*m*sample_rate
        total_liters += average_liters
        db_hz = round(average,4)
        db_liter_by_min= round(average_liters*(60/sample_rate),4)
        print("\t", db_hz,'(hz) average')
        print('\t', db_liter_by_min,'(L/min)') # Display L/min instead of L/sec
        print(round(total_liters,4),'(L) total')
        print(round(secondes/60,4), '(min) total')
        print('-------------------------------------')

    except KeyboardInterrupt:
        print('\n CTRL+C - Exiting')
        GPIO.cleanup()
        #sys.exit()
        break
  GPIO.cleanup()
  print('Done')

def read_flow_sensor(pin_input=8, sample_rate=1):
    
    """Reads water flow sensor and returns (frequency, L/min, total liters, % good samples)."""
    
    GPIO.setup(pin_input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Variables
    time_start = time.time()
    time_end = time_start + sample_rate
    hz = []  
    sample_total_time = 0
    m = 0.0021  # Flow coefficient

    # Edge detection
    current = GPIO.input(pin_input)
    edge = current  

    try:
        while time.time() <= time_end:
            t = time.time()
            v = GPIO.input(pin_input)
            if current != v and current == edge:  # Detect rising edge
                period = t - time_start  
                if period > 0:  # Avoid division by zero
                    new_hz = 1 / period
                    hz.append(new_hz)
                    sample_total_time += t - time_start
                    time_start = t

                    if DEBUG:
                        print(round(new_hz, 4))  # Debugging output

            current = v

        # Processing results
        nb_samples = len(hz)
        if nb_samples > 0:
            average_hz = sum(hz) / nb_samples
            good_sample = sample_total_time / sample_rate
            average_hz *= good_sample  # Adjusted for sample quality
            average_liters = average_hz * m * sample_rate
            total_liters = average_liters  # Since function runs once
            db_good_sample = round(good_sample * 100, 4)
            db_hz = round(average_hz, 4)
            db_liter_by_min = round(average_liters * (60 / sample_rate), 4)
        else:
            db_hz = 0
            db_liter_by_min = 0
            total_liters = 0
            db_good_sample = 0

        return db_liter_by_min
    except KeyboardInterrupt:
        GPIO.cleanup()
        return None
    finally:
        GPIO.cleanup()


