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

from hr_little_api.functional import say
from hr_little_api.robot import Robot


def say_done_cb():
    print("I'm done speaking")


def main():
    #  Instantiate robot object
    robot = Robot()

    # Connect to robot
    if not robot.connect():
        print("Trouble connecting...")
        exit(-1)

    # Non-blocking action, wait for it to complete trigger callback on completion
    ah = robot.do(
        say("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe."),
        block=False, done_cb=say_done_cb)
    robot.wait(ah)

    # Disconnect from robot
    robot.disconnect()


if __name__ == "__main__":
    main()
