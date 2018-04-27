import RPi.GPIO as GPIO
import time
import random
import sys



GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
while True:
    time.sleep(0.1)
    x = GPIO.input(2)
    print(x)
    e = False
    if x is 1:
        e = True
    
    print(e)