"""Play a melody on the buzzer on GP18.

A song is a list of notes, and each note is a name and how many beats it lasts. The NOTES
dictionary turns each name into a pitch in hertz. Wire the buzzer as images/buzzer-circuit.svg
shows, then open this file and click Run.
"""

from machine import PWM, Pin
from time import sleep

# Pitches in hertz, from middle C up to the next C. REST is a silent beat.
NOTES = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "REST": 0,
}

# Seconds in one beat. A smaller number plays the song faster.
BEAT = 0.4

# How loud the buzzer is, from 0 (silent) to 32768 (loudest). Try 2000 for a quieter song.
VOLUME = 32768

# Twinkle, Twinkle, Little Star: each pair is a note's name and its number of beats
TWINKLE = [
    ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
    ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
]

buzzer = PWM(Pin(18))


def play_note(name, beats):
    """Play one note for a number of beats, or stay quiet if it is a rest."""
    pitch = NOTES[name]
    if pitch == 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(pitch)
        buzzer.duty_u16(VOLUME)
    sleep(beats * BEAT * 0.9)
    # A short silence at the end of each note, so two of the same note sound separate
    buzzer.duty_u16(0)
    sleep(beats * BEAT * 0.1)


def play_song(song):
    """Play each note of a song in order."""
    for name, beats in song:
        play_note(name, beats)


play_song(TWINKLE)

# deinit lets go of the pin, so the buzzer stays quiet after the program ends
buzzer.deinit()
