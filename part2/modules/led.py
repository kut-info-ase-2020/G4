import RPi.GPIO as GPIO
import time


class LED():
    def __init__(self, pin):
        self.pin = pin
        self.setup()

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def setup(self):
        GPIO.setwarnings(False)
        #set the gpio modes to BCM numbering
        GPIO.setmode(GPIO.BCM)
        #set LEDPIN's mode to output,and initial level to LOW(0V)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

