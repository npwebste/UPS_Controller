import RPi.GPIO as GPIO
import time

PWMPin = 18 # Pin 18 for PWM
D = .5 # Duty cycle
Freq = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMPin, GPIO.OUT)

PWM = GPIO.PWM(PWMPin, Freq)
pwm.start(D)
print('Starting PWM')

try:
    while 1:
        print('Duty Cycle: {}/n Frequency:{}'.format(D,Freq))
        time.sleep(1)
except KeyboardInterrupt: # CTRL+C
    pass
PWM.stop() # Stop PWM
GPIO.cleanup() # Clean up GPIO pins
