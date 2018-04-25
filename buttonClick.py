import RPi.GPIO as GPIO
import time
import random
import sys



GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
while True:
    time.sleep(0.5)
    x = GPIO.input(2)
    e = False
    if x is 1:
        e = True
    
    print(e)