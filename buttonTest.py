import RPi.GPIO as GPIO
import time
import sys
import random


GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)

# while true:
#     x = GPIO.input(12)
#     if x:
#         print("HELLO")
#         x = false

while True:
    GPIO.output(12,GPIO.HIGH)