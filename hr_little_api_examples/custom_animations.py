#!/usr/bin/python3

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

# Author: James Diprose

from hr_little_api.functional import say, motor, close_mouth, command_list, wait_for_motors_and_speaking, \
    head_turn_middle, neutral_eyebrows, frown_eyebrows, head_turn_right, head_turn_left, poke_tounge, wait, \
    raise_eyebrows, wait_for_motors
from hr_little_api.robot import Robot, MotorId


def main():
    robot = Robot()

    if not robot.connect():
        print("Trouble connecting...")
        exit(-1)

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

    robot.disconnect()


if __name__ == "__main__":
    main()
