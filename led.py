#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


gpio_config = {
    11: GPIO.OUT, # TL1 RED
    13: GPIO.OUT, # TL1 YEL
    15: GPIO.OUT, # TL1 GRN
    16: GPIO.OUT, # TL2 RED
    18: GPIO.OUT, # TL2 GRN
    22: GPIO.OUT, # TL2 YEL
    10: GPIO.IN   # BTN Data
}


pins = {
    'TL1_RED': 11,
    'TL1_YEL': 13,
    'TL1_GRN': 15,
    'TL2_RED': 16,
    'TL2_GRN': 18,
    'TL2_YEL': 22,
    'BTN': 10
}


cycle_tl1 = [
    {
        'leds': ['TL1_RED'],
        'led_state': 'on',
        'duration': 8,
        'system_state': [
            {
                'leds': ['TL2_RED'],
                'led_state': 'on'
            }
        ]
    },
    {
        'leds': ['TL1_RED', 'TL1_YEL'],
        'led_state': 'on',
        'duration': 2
    },
    {
        'leds': ['TL1_GRN'],
        'led_state': 'on',
        'duration': 12
    },
    {
        'loop_cycle': {
                'times': 4,
                'cycle': [
                    {
                        'leds': ['TL1_GRN'],
                        'led_state': 'on',
                        'duration': 1
                    },
                    {
                        'leds': ['TL1_GRN'],
                        'led_state': 'off',
                        'duration': 1
                    }
                ]
            }
    },
    {
        'leds': ['TL1_YEL'],
        'led_state': 'on',
        'duration': 3
    }
]


cycle_tl2 = [
    {
        'leds': ['TL2_GRN'],
        'duration': 12,
        'led_state': 'on',
        'system_state': [
            {
                'leds': ['TL1_RED'],
                'led_state': 'on'
            }
        ],
    },
    {
        'loop_cycle': {
                'times': 4,
                'cycle': [
                    {
                        'leds': ['TL2_GRN'],
                        'led_state': 'on',
                        'duration': 1
                    },
                    {
                        'leds': ['TL2_GRN'],
                        'led_state': 'off',
                        'duration': 1
                    }
                ]
        },
        'next_cycle': {
            'name': 'tl1',
            'start_index': 1
        }
    }
]

cycles = {
    'tl1': cycle_tl1,
    'tl2': cycle_tl2
}


# Create a list of all pins that are wired to LEDs
pins_led = [pin for pin in gpio_config.keys() if gpio_config[pin] == GPIO.OUT]

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
            if led not in pins:
                raise Exception(f'No matching pin found for LED: {led}.')
            else:
                pin = pins[led]
        elif isinstance(led, int):
            if led not in pins_led:
                raise Exception(f'Pin {led} not found in defined LED pins.')
            else:
                pin = led
        else:
            raise Exception(f'Invalid type for LED: {led}.')
    
    if pin != None:
        GPIO.output(pin, gpio_state.get(state))


current_cycle = None
next_cycle = None
next_cycle_name = None

def queue_tl2():
    global current_cycle
    global next_cycle
    global next_cycle_name
    
    if current_cycle == cycles['tl1'] and next_cycle != cycles['tl2']:
        print("Pedestrian cycle queued.")
        leds_on(pins['TL2_YEL'])
        next_cycle = cycles['tl2']
        next_cycle_name = 'tl2'


# Add TL2 cycle to queue.
def button_callback(channel):
    if GPIO.input(pins['BTN']):
        queue_tl2()
    

# Set up all GPIO pins to be inputs or outputs along with event listeners.
def setup_gpio(config):
    config_pins = config.keys()
    
    for pin in config_pins:
        value = gpio_config[pin]
        
        if value == GPIO.OUT:
            GPIO.setup(pin, value)
            
            # LEDs maintain state from last exec, turn off all LEDs just in case.
            leds_off(pin)
            
        elif value == GPIO.IN:
            GPIO.setup(pin, value, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=button_callback)


setup_gpio(gpio_config)

def exec_step(step, system_state_only=False):
    sets_system_state = 'system_state' in step
    is_loop = 'loop_cycle' in step
    has_sub_cycle = 'cycle' in step
    specifies_duration = 'duration' in step
    
    # Set default duration to be 0 to cover for no specified duration.
    duration = 0
    if specifies_duration:
        duration = step['duration']
    
    if sets_system_state:
        system_state = step['system_state']
        for config in system_state:
            leds = config['leds']
            led_state = config['led_state']
            
            leds_state(leds, led_state)
    
    # Skip rest of subcycle exec if only
    # system state needs to be set.
    if system_state_only:
        return
    
    if is_loop:
        loop_cycle = step['loop_cycle']
        for loop_index in range(loop_cycle['times']):
            exec_cycle(loop_cycle['cycle'], True)
    
    if has_sub_cycle:
        exec_cycle(step['cycle'], True)
        
    if not is_loop and not has_sub_cycle:
        leds = step['leds']
        state = step['led_state']
        
        # Set the LEDs to the defined states
        leds_state(leds, state)
        
        time.sleep(duration)
        
        leds_state(leds, 'off')
    

def exec_cycle(cycle, subcycle=False, start_index=0):
    global current_cycle
    global next_cycle
    global next_cycle_name
    
    if not subcycle:
        current_cycle = cycle
        next_cycle = None
        next_cycle_name = None
        next_index = 0
    
    # Reset all LEDs before executing cycle.
    if not subcycle:
        leds_off(pins_led)
    
    for index, step in enumerate(cycle):
        is_last_step = index == len(cycle)-1
        system_state_only = False
        
        # Skip non-system-state info if
        # we are starting the cycle in the middle.
        if index < start_index:
            system_state_only = True
        
        exec_step(step, system_state_only)
        
        if is_last_step and not subcycle:
            first_step = cycle[0]
            has_system_state = 'system_state' in first_step.keys()
            
            # Reset system state configs when cycle ends
            if has_system_state:
                for config in first_step['system_state']:
                    leds_state(config['leds'], 'off')
            
            if next_cycle == None:
                if 'next_cycle' in step.keys():
                    next_cycle = cycles[step['next_cycle']['name']]
                    next_cycle_name = step['next_cycle']['name']
                    next_index = step['next_cycle']['start_index']
                
                # Cycle does not define include next cycle
                else:
                    print('No next cycle specified, using tl1 as next.')
                    next_cycle = cycles['tl1']
                    next_cycle_name = 'tl1'
    
    if not subcycle:
        # Reset all LEDs after executing cycle.
        if not subcycle:
            leds_off(pins_led)
        
        print(f'Next cycle is {next_cycle_name}')
        exec_cycle(next_cycle, start_index=next_index)
        
try:
    # start the recursive function with a default cycle name
    exec_cycle(cycles['tl1'])

except KeyboardInterrupt:
    print("Keyboard interrupt")
finally:
    GPIO.cleanup()


exit()