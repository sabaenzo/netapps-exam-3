#!/usr/local/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, False)

while True:
    GPIO.output(17, True)
    time.sleep(2)
    GPIO.output(17, False)
    time.sleep(2)