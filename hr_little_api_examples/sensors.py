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

import time

from hr_little_api.robot import Robot


def main():
    #  Instantiate robot object, specifying data reading rate as 2Hz
    robot = Robot(read_rate_hz=2)

    # Connect to robot
    if not robot.connect():
        print("Trouble connecting...")
        exit(-1)

    # Wait enough time until data has come in
    time.sleep(3)

    # Read the voltage (a value between 0. and 1.)
    print(robot.voltage)

    # Read the firmware version
    print(robot.version)

    # Disconnect from robot
    robot.disconnect()


if __name__ == "__main__":
    main()
