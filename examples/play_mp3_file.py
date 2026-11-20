"""Play MP3 files with a DFPlayer Mini board and a small speaker.

The buzzer plays one pitch at a time, so a music file needs a DFPlayer Mini: a small board that
reads MP3 files from a microSD card and plays them through a speaker. The Pico sends it short
commands, such as "play file 1" or "set the volume to 20".

To get the card ready on your laptop:
* format the microSD card as FAT32
* make a folder named mp3 on the card
* name the songs 0001.mp3, 0002.mp3, and so on, and put them in that folder

Wiring:
* DFPlayer VCC to VBUS (physical pin 40), which carries 5 volts from the USB cable
* DFPlayer GND to GND
* DFPlayer RX to GP0 (physical pin 1), through a 1k ohm resistor
* the speaker's two wires to SPK_1 and SPK_2 on the DFPlayer
"""

from machine import UART, Pin
from time import sleep

# A UART sends bytes one after another down a single wire, here GP0, at 9600 bits a second
player = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# The DFPlayer's command numbers. Numbers written with 0x are in hexadecimal, the way the
# DFPlayer's manual lists them.
PLAY = 0x12    # play a numbered file from the mp3 folder
VOLUME = 0x06  # set the volume, from 0 to 30
PAUSE = 0x0E
RESUME = 0x0D
STOP = 0x16


def send(command, value):
    """Send one command and its value to the DFPlayer."""
    high = value // 256
    low = value % 256
    # The DFPlayer adds up the message and compares it with this number, to be sure it arrived complete
    checksum = (0 - (0xFF + 0x06 + command + 0x00 + high + low)) % 65536
    message = bytes([0x7E, 0xFF, 0x06, command, 0x00, high, low, checksum // 256, checksum % 256, 0xEF])
    player.write(message)
    sleep(0.1)


# The DFPlayer needs a moment after it powers on to read the card
sleep(2)

send(VOLUME, 20)
send(PLAY, 1)  # plays mp3/0001.mp3
sleep(10)

send(PAUSE, 0)
sleep(2)
send(RESUME, 0)
sleep(10)

send(STOP, 0)
