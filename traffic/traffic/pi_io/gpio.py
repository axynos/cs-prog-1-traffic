import RPi.GPIO as GPIO
from .leds import leds_off
from .button import callback as btn_callback

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set up all GPIO pins to be inputs or outputs along with event listeners.
def setup_gpio(config):
    config_pins = config.keys()
    
    for pin in config_pins:
        value = config[pin]
        
        if value == GPIO.OUT:
            GPIO.setup(pin, value)
            
            # LEDs maintain state from last exec, turn off all LEDs just in case.
            leds_off(pin)
            
        elif value == GPIO.IN:
            GPIO.setup(pin, value, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=btn_callback)