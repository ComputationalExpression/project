"""Read the light sensor on GP26 and turn on the Pico's own LED when the room is dark.

Wire the photoresistor and the 10k ohm resistor as images/light-sensor-circuit.svg shows, then
open this file and click Run. Cover the photoresistor with your hand to see the reading drop.
"""

from machine import ADC, Pin
from time import sleep

# ADC reads the voltage on GP26 as a number from 0 to 65535, which goes up in brighter light
light = ADC(26)
led = Pin("LED", Pin.OUT)

# Readings below this count as dark. Watch the numbers your room gives you, then change it.
DARK = 20000


def brightness_percent(reading):
    """Turn a reading from 0 to 65535 into a percent from 0 to 100."""
    return reading * 100 // 65535


# Twenty readings, two each second
for count in range(20):
    reading = light.read_u16()
    if reading < DARK:
        led.on()
        print(reading, brightness_percent(reading), "percent: dark, light on")
    else:
        led.off()
        print(reading, brightness_percent(reading), "percent: bright, light off")
    sleep(0.5)

led.off()
