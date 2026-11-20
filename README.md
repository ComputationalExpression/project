# CMPSC 100 Final Project

|Item |       |
|:----|:------|
|Released |Monday, November 16, in class |
|Pitch |Monday, November 23, in class |
|Code review |Friday, December 4, at the lab session |
|Due |Monday, December 7, 9:00am |
|Demo fair |Monday, December 7, 9:00am (Exam Code A) |
|Progress |[![Grade](../../actions/workflows/main.yml/badge.svg?branch=main)](../../actions/workflows/main.yml) |

For the final project, you design and build a device of your own on the Pico 2 W. It can be a
game, a tool, an alarm, an instrument, a monitor, or anything else you would like to make, as long
as it reads at least one input, controls at least one output, and is built from classes.

You can work on your own or in a team of two or three.

## Contents

* [Course learning outcomes](#course-learning-outcomes)
* [Timeline](#timeline)
* [Requirements](#requirements)
  * [Working on your own or as a team](#working-on-your-own-or-as-a-team)
* [Hardware](#hardware)
  * [The light sensor](#the-light-sensor)
  * [The buzzer](#the-buzzer)
* [The project report](#the-project-report)
* [Getting started](#getting-started)
* [The pitch](#the-pitch)
* [Code review](#code-review)
* [The demo fair](#the-demo-fair)
* [Evaluation](#evaluation)
* [Using AI](#using-ai)
* [Submitting](#submitting)

## Course learning outcomes

This project addresses the following course learning outcomes:

**CLO 1.** Apply Python programming fundamentals to execute and explain computer code that
implements interactive, novel solutions to a variety of computable problems.

**CLO 2.** Implement code consistent with industry-standard practices using professional-grade
integrated development environments (IDEs), command-line tools, and version control systems.

**CLO 4.** Evaluate the practical and ethical implications of writing computer code and discuss the
contexts, perceived effects, and impacts exerted on and by computer code as a cultural force or
artifact.

**CLO 5.** Design, describe, and implement original projects incorporating industry-standard
practices and Python language fundamentals.

## Timeline

|Date |What happens |
|:----|:------------|
|Monday, November 16 |The project is released. Please start thinking about ideas, and form a team if you would like one |
|Monday, November 23 |You pitch your idea. Before class, please write the first four sections of `docs/report.md`: the idea, the team, the hardware, and the classes |
|November 23 to December 7 |You build the project on branches, merging each part through a pull request |
|Friday, December 4 |Your code review, with a whiteboard, at the lab session |
|Monday, December 7, 9:00am |The project is due on `main`, and the demo fair begins |

## Requirements

Your project needs to:

* run on the Pico 2 W from `src/main.py`, which makes the objects and connects them
* read at least one input (a button, the light sensor, the temperature sensor in the Pico's chip,
  or the DHT22) and control at least one output (an LED or the buzzer)
* keep each class in its own file in `src`, with `__init__` and at least two more methods in each
  class, and at least two methods across the project that return a value
* use at least one list, one dictionary, one loop and one `if` statement
* have a docstring for each class and function, and at least two comments in each file
* be built on branches and merged through at least two pull requests
* have a complete `docs/report.md`

The program can use what we have covered in class and anything else you learn along the way,
provided you can explain it at the code review.

### Working on your own or as a team

|Requirement |On your own |Team of two or three |
|:-----------|:-----------|:--------------------|
|Class files |At least two |At least one for each person, and each person writes their own |
|Hardware |At least one input and one output |At least one input and one output |
|Pull requests |At least two, merged by you |Each person merges their own, after a teammate approves it |
|Pitch and demo fair |One pitch and one demo station |One pitch and one demo station for the team, where each person speaks |
|Code review |One review |One review for each person, about the files they wrote |

Please list your team, and who writes which file, in `docs/report.md` by the pitch. A team accepts
the project once, as a team, through Classroom50.

## Hardware

You can use each part from your kit: the LEDs with their resistors, the push button, the
temperature sensor in the Pico's chip, and the DHT22, as in Labs 5 through 8. A light sensor and a
buzzer are also available. Please ask Dr. Jumadinova for the ones you need by the pitch on
November 23. Remember to unplug the USB cable before you change the wiring.

![The Pico 2 W pinout, with each pin's GP number](images/pico-2-pinout.svg)

### The light sensor

The light sensor is a photoresistor, which lets more current through in brighter light. It needs a
10k ohm resistor beside it:

* one leg of the photoresistor to **3V3(OUT)** (physical pin 36)
* the other leg of the photoresistor to **GP26** (physical pin 31)
* the 10k ohm resistor from **GP26** to **GND**

With this wiring, the reading goes up as the room gets brighter. GP26, GP27 and GP28 can each
read a light sensor.

![A photoresistor and a 10k ohm resistor wired to GP26 on the breadboard](images/light-sensor-circuit.svg)

```python
from machine import ADC

light = ADC(26)
reading = light.read_u16()  # 0 in the dark, up to 65535 in bright light
```

`examples/light_sensor.py` prints twenty readings and turns on the Pico's own LED when the room is
dark. Open it and click **Run**, then cover the photoresistor with your hand to see the reading
drop.

### The buzzer

The buzzer has two legs, and the longer one, marked `+`, goes to a GP pin. The shorter one goes to
**GND**. It sounds when its pin is switched on and off quickly, which `PWM` does for you. `freq` sets
the pitch in hertz, and `duty_u16` turns the sound on (`32768`) or off (`0`).

![A passive buzzer wired to GP18 on the breadboard](images/buzzer-circuit.svg)

```python
from machine import PWM, Pin
from time import sleep

buzzer = PWM(Pin(18))
buzzer.freq(440)        # the note A
buzzer.duty_u16(32768)  # on
sleep(0.5)
buzzer.duty_u16(0)      # off
```

Two programs in `examples` let you try the buzzer before you write your own class. Open one and
click **Run**:

* `buzzer_beep.py` plays a few beeps at different pitches
* `play_melody.py` plays a song from a list of notes, with a dictionary that turns each note's name
  into a pitch

The buzzer plays one pitch at a time, so it can play notes and melodies but not a music file such
as an MP3.

## The project report

`docs/report.md` has six sections. Please write the first four before the pitch, and keep them up
to date as the project changes:

1. **The idea**: what your project does, and who would use it
2. **The team**: "Individual", or each teammate and the class files they write
3. **The hardware**: each part, what it does, and its GP pin
4. **The classes**: a diagram of `main.py` and your classes, with each class's attributes above a
   line and its methods below it, and a few sentences on what each class remembers and does

After the pitch, you write the last two:

5. **The pitch feedback**: two pieces of feedback you received, and what you changed because of each
6. **Reflection**: at least 300 words on your challenges, how you used AI, and an ethical question
   about your project

At the code review, you will draw your class diagram on the whiteboard.

## Getting started

1. **Write your idea and team** in `docs/report.md`.
2. **Plan your classes.** Each thing in your project, such as a sensor, a light, a game or a log,
   can be a class. What it remembers becomes its attributes, and what it does becomes its methods.
   Please see [Your Final Project, slides 6 and 7](https://computationalexpression.com/slides/week-13-session-1/#6).
   Draw the plan in the classes section of `docs/report.md`.
3. **Get one part working first.** Wire one input and one output, and test them with a short
   program on the board before you write the classes.
4. **Build one class at a time**, each on its own branch, and merge it through a pull request.

You can check your work as you go by running this from the project's top-level folder:

```text
uv run gatorgrade --config gatorgrade.yml
```

To run the project on the board, upload each class file first: right-click it in the Explorer,
choose MicroPico, then **Upload File to Board**. Then open `src/main.py` and click **Run** in the bar
along the bottom of the window, with **Board Connected** showing beside it:

![The bar along the bottom of VS Code, showing Board Connected and the Run button](images/run-button.png)

## The pitch

On Monday, November 23, you will pitch your idea in two or three minutes to a small group of
classmates with a Technical Leader or Dr. Jumadinova: what the project does, who would use it, the
hardware, and the classes you plan. Your listeners give you feedback by opening a **Pitch
Feedback** issue on your repository, and you open one on the repository of each classmate whose
pitch you hear. To open one, go to the repository's **Issues** tab, click **New issue**, and choose
**Pitch Feedback**.

## Code review

Your code review is at the lab session on Friday, December 4, with a Technical Leader or the
instructor. It is a conversation about your code, and you do not need to run the project for it.
You will draw your class diagram on the whiteboard and answer questions about the code you wrote.
In a team, each person has their own review, about the files they wrote. The reviewer opens a
**Code Review** issue on your repository. The questions differ from student to student, so please
be ready to:

* **Classes and objects**: explain what each of your classes remembers and does, and how `main.py`
  connects them
* **Methods and self**: trace one of your methods on the whiteboard, with the value of each
  attribute before and after
* **Data**: explain what your list and dictionary hold, and trace a loop over one of them
* **Decisions**: explain one of your `if` statements, and what happens at its edge, such as a
  reading exactly at a dividing value
* **Hardware**: explain how your code reads its input and controls its output, and which pins they
  use

If you cannot attend that lab, please arrange your review beforehand at office hours.

## The demo fair

The demo fair is during the final exam slot, on Monday, December 7, at 9:00am. Half of the class
sets up their projects at stations while the other half visits, and the two halves swap at the
midpoint. When it is your turn at a station, you will run your project on the board and explain in
two or three minutes what it does and how it works, to each small group that visits. When it is
your turn to visit, you will fill in a feedback sheet for each project you see.

## Evaluation

The project is worth **18 points**.

| Component | Points | What it measures |
|:----------|:-------|:-----------------|
| Pitch | 2 | The first four sections of `docs/report.md` written before the pitch (1), and your pitch with the Pitch Feedback issues you opened for classmates (1) |
| Program | 8 | The 15 checks below, as a fraction of 4 points; code quality in the files you wrote: descriptive names, clear organization and useful comments (2); the first five sections of `docs/report.md` complete and matching the code (1); the reflection (1) |
| Code review | 5 | One point for each of the five topics above, answered about your own code on the whiteboard |
| Demo fair | 3 | The project running on the board at your station (1), your explanation of how it works (1), and your feedback sheets for classmates' projects (1) |
| **Total** | **18** | |

In a team, the checks and the first five sections of the report are shared. The code quality
score, the code review, the feedback sheets and the reflection are your own, so each teammate
writes their own reflection under a heading with their name.

You can run the checks yourself, as many times as you like:

```text
uv run gatorgrade --config gatorgrade.yml
```

Each check's description says what to look at when it fails. Under a failed check, gatorgrade
also prints a `uv run pytest ...` command, and when you run it, the last lines tell you what was
found and what was expected. These are the fifteen checks:

* `src/main.py` has a docstring and a `main()` function, and imports classes from at least two of
  your class files
* at least two files in `src` besides `main.py` each define a class, and a team has at least one
  for each person
* each class has `__init__` and at least two more methods
* at least two methods return a value with `return`
* each class and function has a docstring
* the code reads an input: a `Pin` with `Pin.IN`, an `ADC`, or a `dht.DHT22`
* the code controls an output: a `Pin` with `Pin.OUT`, or a `PWM`
* the code uses a list and a dictionary
* the code uses a loop and an `if` statement
* Python can load each class file without an error. The check does this on your laptop with
  stand-ins for the Pico's `machine` and `dht` modules, so it finds a typo, a missing import or a
  misspelled name without your board
* no `TODO` markers remain in `src`
* each file in `src` has at least two comments
* at least two pull requests are merged on GitHub with the **Merge pull request** button, rather
  than **Squash and merge**, which leaves no merge in the history
* no `TODO` markers remain in `docs/report.md`
* the Reflection section of `docs/report.md` has at least 300 words of your own

The checks read the shape of your code without running it, so the demo fair is where your
project shows that it works.

> [!NOTE]
> Automated results are preliminary. Your instructor sets the final grade.

## Using AI

On this project, you may use AI in three ways:

* **Code completion**: Copilot's gray suggestions as you type, which this repository turns on.
  Accept them one word or one line at a time, as in Activity 10, and keep only lines you can
  explain
* **Testing**: deciding which cases to try on the board, and which values sit at the edge of an
  `if`
* **Brainstorming**: talking through ideas, features, parts and a class plan in Copilot Chat

Copilot Chat does not write code for you in this repository, and code written for you by any other
AI tool is not allowed. At the code review, you trace and explain your own code on the
whiteboard. Please describe in the reflection which tools you used, what you asked them, and which
parts of your code they helped with.

## Submitting

The `main` branch on GitHub at 9:00am on Monday, December 7, is what gets graded, so please merge
your pull requests before then. Late tokens cannot be used on the final project.
