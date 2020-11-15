from ..cycles.cycles import queue_tl2
from .constants import PINS
import RPi.GPIO as GPIO

def callback(channel):
    if GPIO.input(PINS['BTN']):
        queue_tl2()