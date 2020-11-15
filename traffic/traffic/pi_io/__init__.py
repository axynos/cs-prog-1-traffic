from . import gpio
from .constants import GPIO_CONFIG
import RPi.GPIO as GPIO


gpio.setup_gpio(GPIO_CONFIG)

def cleanup():
    GPIO.cleanup()