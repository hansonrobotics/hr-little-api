hr-little-api
=============
The **hr-little-api** is a Python 3 module that lets you program Hanson Robotics consumer robots.

## Contents
- [Dependencies](#dependencies): what you need before getting started.
- [Installation from PyPI](#installation-from-pypi): how to install hr-little-api from PyPI with pip.
- [Installation from source](#installation-from-source): how to install hr-little-api from source.
- [Quick Start](#quick-start): how to get started programming your robot.
- [Running Examples](#running-examples): how to run the pre-made example programs.
- [Running Examples From Source](#running-examples-from-source): how to run the pre-made example programs from source.
- [Code Documentation](#code-documentation): more comprehensive API documentation, coming soon!
- [Acknowledgements and License](#acknowledgements-and-license)

## Dependencies
To follow these tutorials you will need:
* A Professor Einstein robot.
* Python 3.6 or greater.
* A computer with WiFi: Linux, Windows or MacOS X.

## Installation from PyPI
To install hr-little-api from PyPI, with the command line using pip:
```python
pip3 install hr-little-api
```

## Installation from source
Clone project from Github
```bash
git clone https://github.com/jdddog/hr_little_api
```

Enter folder
```bash
cd hr_little_api
```

Install with pip
```bash
pip3 install -e .
```

## Quick Start
The hr-little-api lets you program Hanson Robotics consumer robots. Follow this tutorial to get an overview of 
how to use the API and it's various features.

### Setting up your robot
Turn on Professor Einstein with the power button on at the back:

![Professor Einstein on/off button](https://github.com/jdddog/consumer_robot_api/blob/master/docs/einstein_power.jpg?raw=true)

When your robot starts up, it should say:
> Ok here we go, just one, I don't see any WiFi networks I recognize, go to the connection channel in your Stein-O-Matic
> to solve your problem.

To program Professor Einstein, you will need his WiFi SSID and password. To find this, press the `Binding Button` as 
shown in the image below:

![Binding button](https://github.com/jdddog/consumer_robot_api/blob/master/docs/einstein_binding_button.jpg?raw=true)

Professor Einstein should then say the following:
> Go to your device settings and look for network EinsteinXXXX my password is geniusXXXX.

Connect your computer to the Professor Einstein WiFi network using the given SSID and password. If successful the
Professor should say the following:
> So far so good I just need another moment or two so I can finish logging you in. That did the trick, now return to the
> Stein-O-Matic to continue.

You are all set and ready to go!

### Robot class, connecting and disconnecting from the robot
The `Robot` class enables you to control your robot, but before we can do this we need to connect to the robot's
network.

First import the `Robot` object from hr_little_api:
```python
from hr_little_api.robot import Robot
```

Instantiate a `Robot` object.
```python
robot = Robot()
```

Before controlling the robot, make sure you call `robot.connect` and before your program exits call `robot.disconnect`
to close the connection with the robot.
```python
if not robot.connect():
    print("Trouble connecting...")
    exit(-1)
    
### Your code here ###

robot.disconnect()
```

### Robot actions: say, walk and animate
The `Robot` class has a number of methods to help you issue actions to the robot, these enable it to speak,
walk and play animations.

To make the robot speak, call the `robot.say` method with the text that you want the robot to say:
```python
robot.say('Hello I am Professor Einstein, here we go!')
```

By default actions block until the action has finished. As of this writing, you can only issue one set of commands
at a time to the robot. If you want the robot to speak and animate simultaneously then look at the [Functional API](#functional-api-intro).

To make the robot walk, execute following commands:
```python
robot.walk_forward()
robot.walk_backward()
robot.walk_left()
robot.walk_right()
```

You may control the number of steps that the robot takes with the `steps` parameter, an integer between 1 and 10:
```python
robot.walk_forward(steps=10)  # Both of my feet will step forward 10 times each.
robot.walk_left(steps=10)  # My right foot will step forward 10 times, making me walk left.
```

To animate the robot, import the `Animation` enum, which contains the pre-defined animations that Professor Einstein 
can make. Call the `robot.animate` method supplying it with an `Animation` enum member which indicates which animation
to play.
```python
from hr_little_api.robot import Animation
robot.animate(Animation.poke_tounge)
robot.animate(Animation.right_arm_point)
robot.animate(Animation.sleep)
robot.animate(Animation.wake_up)
```

### Robot sensors: read sensory data
The `Robot` class has instance attributes for reading the robot's voltage and reading the firmware version.
 
To read the voltage (a value between 0. and 1.):
```python
print(robot.voltage)
```

To read the firmware version:
```python
print(robot.version)
```

You can control the rate sensory data is updated via the `read_rate_hz` class parameter (by default this is set to 1Hz),
here we set it to 2Hz:
```python
robot = Robot(read_rate_hz=2)
```

### Non-blocking actions and callbacks
Actions can also be run in non-blocking mode where a callback is received after the action has completed.

Define a callback function:
```python
def say_done_cb():
    print("I'm done speaking")
```

When calling a robot action method, specify `block=False` and assign your function name to the `done_cb` parameter. You
can call the `robot.wait` method to wait for the action to complete.
```python
# Non-blocking action, wait for it to complete trigger callback on completion
ah = robot.say("If you can't explain it simply, you don't understand it well enough.", block=False,
               done_cb=say_done_cb)
robot.wait(ah)
```

### Functional API: intro
The hanson-little-api also provides a functional API for finer control of robot actions, enabling simultaneous 
speaking and animation and authoring of custom animations.

Let's go through a few simple examples.

Start by importing the functions we will use in these examples:
```python
from hr_little_api.functional import say, go_crazy, poke_tounge, right_arm_point, walk_forward
```

With the functional API, we create actions by calling functions that represent the action we want the robot make,
and then pass the action function to the `robot.do` function.

For example, to make the robot speak:
```python
robot.do(say("Have you seen my cousin Zoidstein?"))
```

To make the robot play an animation:
```python
robot.do(poke_tounge())
```

To make the robot walk:
```python
robot.do(walk_forward())
```

### Functional API: simultaneous actions
With the functional API, we can combine various actions together, to enable the robot to speak and animate or
speak and walk at the same time.

To speak and animate at the same time:
```python
robot.do(say("Zoidstein is an abomination"), go_crazy())
```

To speak, animate and walk at the same time:
```python
robot.do(
    say("I'm outta here before he nips me with his pincers!"),
    right_arm_point(),
    walk_forward()
)
```

The following can be played at the same time:
* Speaking and all other actions.
* All pre-defined animations and walking.
* Pre-defined short animations, e.g. `right_arm_point` and `poke_tounge`.

The following cannot be played at the same time:
* Pre-defined long animations - only one at a time, e.g. `go_crazy` and `awkward`.

### Functional API: writing your own animations
The functional API enables you to write your own animations, create reusable animation blocks and directly control
the robot's motors.

Start by importing the functions we will need for these examples:
```python
from hr_little_api.functional import say, motor, close_mouth, command_list, wait_for_motors_and_speaking, \
    head_turn_middle, neutral_eyebrows, frown_eyebrows, head_turn_right, head_turn_left, poke_tounge, wait, \
    raise_eyebrows, wait_for_motors
from hr_little_api.robot import Robot, MotorId
```

When creating custom animations, there are few commands that will be helpful, including:
* `wait_for_motors`: blocks until previous motor commands have finished moving, but doesn't wait for speech.
* `wait`: waits a set period of time, doesn't wait for speech.
* `wait_for_motors_and_speaking`: waits until all previous speech commands have finished.

The example below shows you how to create a more advanced custom animation than what we have seen so far:
```python
# Custom action using pre-defined animation primitives
robot.do(
    say("Insanity: doing the same thing over and over again and expecting different results."),

    raise_eyebrows(),
    head_turn_left(),
    wait_for_motors(),  # all previous active motor commands run in parallel
    wait(0.5),  # wait for 0.5 seconds until next motor command, but keep speaking

    frown_eyebrows(),
    head_turn_right(),
    wait_for_motors(),  # all previous active motor commands run in parallel
    wait(0.5),  # wait for 0.5 seconds until next motor command, but keep speaking

    raise_eyebrows(),
    head_turn_left(),
    wait_for_motors(),  # all previous active motor commands run in parallel
    wait(0.5),  # wait for 0.5 seconds until next motor command, but keep speaking

    frown_eyebrows(),
    head_turn_right(),
    wait_for_motors(),  # all previous active motor commands run in parallel
    wait(0.5),  # wait for 0.5 seconds until next motor command, but keep speaking

    neutral_eyebrows(),
    head_turn_middle(),
    wait_for_motors_and_speaking(),  # wait until active speaking and motor commands have finished.

    poke_tounge(),
    wait(1.5),  # wait for 1.5 seconds
    close_mouth()
)
```

You can also control motors directly and create reusable animation blocks.

To control a motor directly use the `motor` function. You indicate the motor to move with the MotorId enum, the position
the motor should move to with the `position` parameter (from 0.0 to 1.0) and control the time that the motor takes to
move with the `seconds` parameter (a lower value means the motor moves faster). An example is illustrated below.
```python
motor(MotorId.eyebrows, 0.0, 0.5)
```

To create a reusable animation block input commands into the `command_list` function, which you can pass to the 
`robot.do` method. A complete example of the above concepts is shown below:
```python
# Custom reusable action using motor primitives, return this from a function if you want it to be consistent
# with the other animations
cheeky_eyebrow_raise_cmd = command_list(
    motor(MotorId.eyebrows, 0.0, 0.5),  # move the eyebrow motor to position 0.0 in 0.5 seconds
    wait_for_motors(),  # wait until previous motor command has finished
    wait(0.1),  # wait for a time

    motor(MotorId.eyebrows, 1.0, 0.5),  # move the eyebrow motor to position 1.0 in 0.5 seconds
    wait_for_motors(),
    wait(0.1)
)

poke_tounge_cmd = command_list(
    poke_tounge(),
    wait_for_motors(),  # wait for previous motor commands to finish
    wait(1.5),  # wait for 1.5 seconds
    
    close_mouth(),
    wait_for_motors(),  # wait for mouth to close
)

robot.do(
    say("Imagination is everything. It is the preview of life's coming attractions."),
    wait(1.0),

    cheeky_eyebrow_raise_cmd,
    cheeky_eyebrow_raise_cmd,
    cheeky_eyebrow_raise_cmd,
    cheeky_eyebrow_raise_cmd,
    wait_for_motors_and_speaking(),

    poke_tounge_cmd
)
```

### Functional API: non blocking actions and callbacks
Functional commands can also be run in non-blocking mode where a callback is received after the commands have completed.

Define a callback function:
```python
def say_done_cb():
    print("I'm done speaking")
```

When calling `robot.do`, specify `block=False` and assign your function name to the `done_cb` parameter. You
can call the `robot.wait` method to wait for the action to complete.
```python
ah = robot.do(
    say("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe."),
    block=False, done_cb=say_done_cb)
robot.wait(ah)
```

## Running Examples
If you installed hr-little-api from PyPI with pip, the example programs should be installed on your system. See
below of the commands to run them from a terminal.

Make the robot play example actions:
```bash
hr_little_api_actions
```

Read data from sensors:
```bash
hr_little_api_sensors
```

Action callback example:
```bash
hr_little_api_action_callbacks
```

Functional API examples:
```bash
hr_little_api_functional_api
```

Functional API callback example:
```bash
hr_little_api_functional_api_callbacks
```

Custom animations:
```bash
hr_little_api_custom_animations
```

## Running Examples From Source
See below for instructions on how to run the example programs from source.

Navigate to the examples directory:

```bash
cd hr-little-api/hr_little_api_examples
```

Make the robot play example actions:
```python
python3 actions.py
```

Read data from sensors:
```python
python3 sensors.py
```

Action callback example:
```python
python3 action_callbacks.py
```

Functional API examples:
```python
python3 functional_api.py
```

Functional API callback example:
```python
python3 functional_api_callback.py
```

Custom animations:
```python
python3 custom_animations.py
```

## Code Documentation
Coming soon...

## Acknowledgements and License
We would like to acknowledge the following people: Vytas Krisciunas, Ean Schuessler, Frank Chernek, Jeanne Lim, 
Desmond Germans, Stephane Leroy, Ivan Lee, Paul Bridges, Ralf Mayet, Jamie Diprose, Mengna Lei, Jessica Freeny, 
Mandeep Bhatia, David Hanson, Hanson Robotics, Centek; and special thanks to Andy Rifkin and his team for the 
original professor Einstein product design and execution.

The hr-little-api project is released under the following license:
```bash
# Copyright 2019 Hanson Robotics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```
