import RPi.GPIO as GPIO
from .constants import PINS_LED
from .constants import PINS

# Helper functions for LED state management.
def leds_on(led_leds):
    leds_state(led_leds, 'on')

def leds_off(led_leds):
    leds_state(led_leds, 'off')

def leds_state(led_leds, state='off'):
    gpio_state = {
        'on': GPIO.HIGH,
        'off': GPIO.LOW
    }
    
    pin = None
    
    if not isinstance(led_leds, list):
        led_leds = [led_leds]
    
    for led in led_leds:
        if isinstance(led, str):
            if led not in PINS:
                raise Exception(f'No matching pin found for LED: {led}.')
            else:
                pin = PINS[led]
        elif isinstance(led, int):
            if led not in PINS_LED:
                raise Exception(f'Pin {led} not found in defined LED pins.')
            else:
                pin = led
        else:
            raise Exception(f'Invalid type for LED: {led}.')
    
    if pin != None:
        GPIO.output(pin, gpio_state.get(state))