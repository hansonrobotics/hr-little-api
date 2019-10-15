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

from hr_little_api.robot import Robot, Animation


def main():
    #  Instantiate robot object
    robot = Robot()

    # Connect to robot
    if not robot.connect():
        print("Trouble connecting...")
        exit(-1)

    # Robot actions: say, walk and animate
    print("Speak")
    robot.say('Hello I am Professor Einstein, here we go!')

    print("Walk forward")
    robot.walk_forward()

    print("Walk backward")
    robot.walk_backward()

    print("Walk left")
    robot.walk_left()

    print("Walk right")
    robot.walk_right()

    print("Animate: right_arm_down")
    robot.animate(Animation.right_arm_down)

    print("Animate: right_arm_point")
    robot.animate(Animation.right_arm_point)

    print("Animate: head_down")
    robot.animate(Animation.head_down)

    print("Animate: head_middle")
    robot.animate(Animation.head_middle)

    print("Animate: head_up")
    robot.animate(Animation.head_up)

    print("Animate: head_turn_left")
    robot.animate(Animation.head_turn_left)

    print("Animate: head_turn_middle")
    robot.animate(Animation.head_turn_middle)

    print("Animate: head_turn_right")
    robot.animate(Animation.head_turn_right)

    print("Animate: close_mouth")
    robot.animate(Animation.close_mouth)

    print("Animate: open_mouth")
    robot.animate(Animation.open_mouth)

    print("Animate: poke_tounge")
    robot.animate(Animation.poke_tounge)

    print("Animate: eye_lid_open")
    robot.animate(Animation.eye_lid_open)

    print("Animate: eye_lid_close")
    robot.animate(Animation.eye_lid_close)

    print("Animate: raise_eyebrows")
    robot.animate(Animation.raise_eyebrows)

    print("Animate: raise_eyebrows")
    robot.animate(Animation.raise_eyebrows)

    print("Animate: frown_eyebrows")
    robot.animate(Animation.frown_eyebrows)

    print("Animate: smile")
    robot.animate(Animation.smile)

    print("Animate: mouth_neutral")
    robot.animate(Animation.mouth_neutral)

    print("Animate: mouth_frown")
    robot.animate(Animation.mouth_frown)

    print("Animate: go_crazy")
    robot.animate(Animation.go_crazy)

    print("Animate: awkward")
    robot.animate(Animation.awkward)

    print("Animate: cute1")
    robot.animate(Animation.cute1)

    print("Animate: cute2")
    robot.animate(Animation.cute2)

    print("Animate: sleep")
    robot.animate(Animation.sleep)

    # Note the following longer running animations sometimes have problems... you may have to restart the robot if so.
    # print("Animate: sleeping")
    # robot.animate(Animation.sleeping)
    #
    # print("Animate: sleepy")
    # robot.animate(Animation.sleepy)
    #
    # print("Animate: tell_a_joke")
    # robot.animate(Animation.tell_a_joke)
    #
    # print("Animate: wake_up")
    # robot.animate(Animation.wake_up)
    #
    # print("Animate: worry")
    # robot.animate(Animation.worry)

    # Disconnect from robot
    print("Disconnect")
    robot.disconnect()


if __name__ == "__main__":
    main()
