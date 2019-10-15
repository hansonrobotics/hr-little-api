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

from hr_little_api.functional import say, go_crazy, poke_tounge, right_arm_point, walk_forward
from hr_little_api.robot import Robot


def main():
    robot = Robot()

    if not robot.connect():
        print("Trouble connecting...")
        exit(-1)

    print("Functional say command")
    robot.do(say("Have you seen my cousin Zoidstein?"))

    print("Functional animation")
    robot.do(poke_tounge())

    print("Combining speaking with animations")
    robot.do(say("Zoidstein is an abomination"), go_crazy())
    robot.do(
        say("I'm outta here before he nips me with his pincers!"),
        right_arm_point(),
        walk_forward()
    )

    robot.disconnect()


if __name__ == "__main__":
    main()
