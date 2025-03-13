#!/usr/bin/env python
#DEBUG = True
DEBUG = False
import time, sys
import RPi.GPIO as GPIO
from datetime import datetime

def loop_sensor():
  # configurations
  pin_input = int(10)
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

def read_sensor_liters():
    # Configurations
    pin_input = 10  # No need for int(10), just use 10
    sample_time = 1  # Read for 1 second
    conversion_factor = 0.0021  # Liters per pulse

    # Ensure a clean start
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)  # Must be set before setup
    GPIO.setup(pin_input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Remove previous event detection if it exists
    if GPIO.gpio_function(pin_input) == GPIO.IN:
        GPIO.remove_event_detect(pin_input)

    pulse_count = 0

    print("Water Flow - YF-S201 measurement")

    # Callback function to count pulses
    def pulse_callback(channel):
        nonlocal pulse_count
        pulse_count += 1

    try:
        # Setup event detection
        GPIO.add_event_detect(pin_input, GPIO.RISING, callback=pulse_callback)
        
        # Wait for the sample period
        time.sleep(sample_time)

    except RuntimeError as e:
        print(f"GPIO Error: {e}")
    
    finally:
        GPIO.remove_event_detect(pin_input)  # Clean up event detection
        GPIO.cleanup()  # Clean up GPIO settings

    # Calculate flow rate
    flow_rate_lpm = pulse_count * conversion_factor * 60 / sample_time
    #print('-------------------------------------')
    #print('Current Time:', time.asctime(time.localtime()))
    #print(f'Pulses detected: {pulse_count}')
    #print(f'Flow rate: {flow_rate_lpm:.4f} L/min')
    #print(f'Total liters: {pulse_count * conversion_factor:.4f} L')
    #print('-------------------------------------')
    return flow_rate_lpm;

