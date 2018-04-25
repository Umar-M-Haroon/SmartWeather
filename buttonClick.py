import RPi.GPIO as GPIO
import time
import random
import sys



GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
while True:
    print(GPIO.input(2))