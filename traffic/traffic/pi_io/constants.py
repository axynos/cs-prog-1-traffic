import RPi.GPIO as GPIO

GPIO_CONFIG = {
    11: GPIO.OUT, # TL1 RED
    13: GPIO.OUT, # TL1 YEL
    15: GPIO.OUT, # TL1 GRN
    16: GPIO.OUT, # TL2 RED
    18: GPIO.OUT, # TL2 GRN
    22: GPIO.OUT, # TL2 YEL
    10: GPIO.IN   # BTN Data
}


PINS = {
    'TL1_RED': 11,
    'TL1_YEL': 13,
    'TL1_GRN': 15,
    'TL2_RED': 16,
    'TL2_GRN': 18,
    'TL2_YEL': 22,
    'BTN': 10
}


# Create a list of all pins that are wired to LEDs
PINS_LED = [pin for pin in GPIO_CONFIG.keys() if GPIO_CONFIG[pin] == GPIO.OUT]
PIN_BUTTON = PINS['BTN']