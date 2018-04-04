import RPi.GPIO as GPIO
import time

Pin = XX # Pin XX for GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin, GPIO.IN)

try:
    while 1:
		i = GPIO.input()
        print()
        time.sleep(1)
except KeyboardInterrupt: # CTRL+C
    pass
PWM.stop() # Stop PWM
GPIO.cleanup() # Clean up GPIO pins
