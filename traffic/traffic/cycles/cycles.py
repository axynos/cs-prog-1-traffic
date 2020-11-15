from .constants import CYCLES as cycles
from ..pi_io.leds import *
from ..pi_io.constants import PINS_LED
from ..pi_io.constants import PINS
import time

current_cycle = None
next_cycle = None
next_cycle_name = None

def queue_tl2():
    global current_cycle
    global next_cycle
    global next_cycle_name
    
    if current_cycle == cycles['tl1'] and next_cycle != cycles['tl2']:
        print("Cycle tl2 queued.")
        leds_on(PINS['TL2_YEL'])
        next_cycle = cycles['tl2']
        next_cycle_name = 'tl2'

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
        leds_off(PINS_LED)
    
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
            leds_off(PINS_LED)
        
        print(f'Next cycle is {next_cycle_name}')
        exec_cycle(next_cycle, start_index=next_index)