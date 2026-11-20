"""Beep the buzzer on GP18.

Wire the buzzer as images/buzzer-circuit.svg shows, then open this file and click Run.
"""

from machine import PWM, Pin
from time import sleep

# PWM switches the pin on and off very quickly, and that is what makes the buzzer sound
buzzer = PWM(Pin(18))

# duty_u16 takes a number from 0 to 65535. Half of that is the loudest, and 0 is silent.
ON = 32768
OFF = 0


def beep(pitch, seconds):
    """Sound the buzzer at a pitch in hertz for some seconds, then stop."""
    buzzer.freq(pitch)
    buzzer.duty_u16(ON)
    sleep(seconds)
    buzzer.duty_u16(OFF)


# Three short beeps at the same pitch, with a pause after each one
for count in range(3):
    beep(1000, 0.2)
    sleep(0.2)

# A low beep and then a high one, so you can hear how the pitch changes
beep(300, 0.5)
beep(1500, 0.5)

# deinit lets go of the pin, so the buzzer stays quiet after the program ends
buzzer.deinit()
