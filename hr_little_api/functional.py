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

from hr_little_api.builders import MotorCommandBuilder, SayCommandBuilder, \
    WalkCommandBuilder, MotorId, WalkDirection, WaitCommandBuilder, WaitType, CallbackCommandBuilder, CallbackType, \
    CommandListBuilder

""" The following functions are used to make the robot speak, walk, move it's motors and to combine multiple 
commands together. """


def say(text: str) -> SayCommandBuilder:
    """ Make the robot speak.

    :param text: the text for the robot to speak.
    :return: a say command.
    """

    return SayCommandBuilder(text)


def walk_forward(steps: int = 4) -> WalkCommandBuilder:
    """ Make the robot walk forward a given number of steps.

    :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means both feet step
    forward once time each.
    :return: a walk forward command.
    """

    return WalkCommandBuilder(WalkDirection.forward, steps=steps)


def walk_backward(steps: int = 4) -> WalkCommandBuilder:
    """ Make the robot walk backward a given number of steps.

    :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means both feet step
    backward once time each.
    :return: a walk backward command.
    """

    return WalkCommandBuilder(WalkDirection.backward, steps=steps)


def walk_left(steps: int = 4) -> WalkCommandBuilder:
    """ Make the robot walk left a given number of steps.

    :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means the right foot takes
    a single step, making the robot walk left.
    :return: a walk left command.
    """

    return WalkCommandBuilder(WalkDirection.left, steps=steps)


def walk_right(steps: int = 4) -> WalkCommandBuilder:
    """ An action to make the robot walk right a given number of steps.

    :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means the left foot takes
    a single step, making the robot walk right.
    :return: a walk right command.
    """

    return WalkCommandBuilder(WalkDirection.right, steps=steps)


def motor(motor_id: MotorId, position: float, seconds: float) -> MotorCommandBuilder:
    """ Move a motor, to a given position in a given time (seconds)

    :param motor_id: the ID of the motor.
    :param position: the position to move the motor to, between 0.0 and 1.0.
    :param seconds: the time in seconds that the motor should take to move to the desired position, between 0.0 and
    10.0.
    :return: a motor command.
    """

    return MotorCommandBuilder(motor_id, position, seconds)


def command_list(*commands) -> CommandListBuilder:
    """ Creates a list of commands.

    :param commands: the list of commands to concatenate together.
    :return: a list of commands.
    """

    cmd_list = [cmd for cmd in commands]
    return CommandListBuilder(cmd_list)


""" The following functions are used to wait for motors and speech commands to start or finish, useful when building 
custom animations """


def wait_for_motors() -> WaitCommandBuilder:
    """ Wait until previous motor commands have finished.

    :return: the wait for motors command.
    """

    return WaitCommandBuilder(WaitType.wait_for_motors)


def wait_for_motors_and_speaking() -> WaitCommandBuilder:
    """ Wait until previous motor and say commands have finished.

    :return: the wait for motors and speaking command.
    """

    return WaitCommandBuilder(WaitType.wait_for_motors_and_speaking)


def wait(seconds: float) -> WaitCommandBuilder:
    """ Wait for a given number of seconds.

    :return: the wait a given number of seconds command.
    """

    return WaitCommandBuilder(WaitType.wait, seconds=seconds)


def wait_for_say_start() -> WaitCommandBuilder:
    """ Wait until the previous say command has started.

    :return: the wait for say command.
    """

    return WaitCommandBuilder(WaitType.wait_for_say_start)


def wait_for_say_done() -> WaitCommandBuilder:
    """ Wait until previous say command has finished.

    :return: the wait for speaking done command.
    """

    return WaitCommandBuilder(WaitType.wait_for_say_done)


""" Callback functions are used to indicate if a callback should be sent before or after an action. These are used 
internally within the API.
"""


def callback_start(callback_id: str) -> CallbackCommandBuilder:
    """ Make a trigger start command, which makes the robot send a trigger message when a command starts. Only works
    for speaking commands.

    :param callback_id: a unique string that the robot will send to you.
    :return: the callback start command.
    """

    return CallbackCommandBuilder(CallbackType.start, callback_id)


def callback_end(callback_id: str) -> CallbackCommandBuilder:
    """ Make a trigger end command, which makes the robot send a trigger message when a command finishes. Only works
    for speaking commands.

    :param callback_id: a unique string that the robot will send to you.
    :return: the callback end command.
    """

    return CallbackCommandBuilder(CallbackType.end, callback_id)


""" The following functions provide user friendly descriptions for common motor commands;
these are atomic animations. """


def right_arm_down(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Move the right arm down.

    :param seconds: the time in seconds for the animation to run for.
    :return: the right arm down command.
    """

    return motor(MotorId.right_arm, 0, seconds)


def right_arm_point(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Point the right arm.

    :param seconds: the time in seconds for the animation to run for.
    :return: the point right arm command.
    """

    return motor(MotorId.right_arm, 1, seconds)


def head_down(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Pitch head down.

    :param seconds: the time in seconds for the animation to run for.
    :return: the head down command.
    """

    return motor(MotorId.head_pitch, 0, seconds)


def head_middle(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Pitch head to middle.

    :param seconds: the time in seconds for the animation to run for.
    :return: the head middle command.
    """

    return motor(MotorId.head_pitch, 0.5, seconds)


def head_up(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Pitch the head up.

    :param seconds: the time in seconds for the animation to run for.
    :return: the head up command.
    """

    return motor(MotorId.head_pitch, 1, seconds)


def head_turn_left(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Turn the head left.

    :param seconds: the time in seconds for the animation to run for.
    :return: the head turn left command.
    """

    return motor(MotorId.head_turn, 1, seconds)


def head_turn_middle(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Turn the head to the middle.

    :param seconds: the time in seconds for the animation to run for.
    :return: the head turn middle command.
    """

    return motor(MotorId.head_turn, 0.5, seconds)


def head_turn_right(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Turn the head right.

    :param seconds: the time in seconds for the animation to run for.
    :return: head turn right command.
    """

    return motor(MotorId.head_turn, 0.0, seconds)


def close_mouth(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Close mouth.

    :param seconds: the time in seconds for the animation to run for.
    :return: the close mouth command.
    """

    return motor(MotorId.mouth, 0, seconds)


def open_mouth(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Open mouth.

    :param seconds: the time in seconds for the animation to run for.
    :return: the open mouth command.
    """

    return motor(MotorId.mouth, 0.5, seconds)


def poke_tounge(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Poke tounge out.

    :param seconds: the time in seconds for the animation to run for.
    :return: the poke touge out command.
    """

    return motor(MotorId.mouth, 1, seconds)


def eye_lid_open(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Open eye lids.

    :param seconds: the time in seconds for the animation to run for.
    :return: the eye lid open command.
    """

    return motor(MotorId.eyelids, 0, seconds)


def eye_lid_close(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Close eye lids.

    :param seconds: the time in seconds for the animation to run for.
    :return: the close eye lids command.
    """

    return motor(MotorId.eyelids, 1, seconds)


def raise_eyebrows(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Raise eyebrows.

    :param seconds: the time in seconds for the animation to run for.
    :return: the raise eyebrows command.
    """

    return motor(MotorId.eyebrows, 0, seconds)


def neutral_eyebrows(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Make eyebrows neutral.

    :param seconds: the time in seconds for the animation to run for.
    :return: the neutral eyebrows command.
    """

    return motor(MotorId.eyebrows, 0.5, seconds)


def frown_eyebrows(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Frown eyebrows.

    :param seconds: the time in seconds for the animation to run for.
    :return: the frown eyebrows command.
    """

    return motor(MotorId.eyebrows, 1, seconds)


def smile(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Smile.

    :param seconds: the time in seconds for the animation to run for.
    :return: the smile command.
    """

    return motor(MotorId.lip_corners, 0, seconds)


def mouth_neutral(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Mouth neutral.

    :param seconds: the time in seconds for the animation to run for.
    :return: the mouth neutral command.
    """

    return motor(MotorId.lip_corners, 0.5, seconds)


def mouth_frown(seconds: float = 0.5) -> MotorCommandBuilder:
    """ Frown mouth.

    :param seconds: the time in seconds for the animation to run for.
    :return: the frown mouth command.
    """

    return motor(MotorId.lip_corners, 1, seconds)


""" The following functions are pre-defined long running animations. """


def reset_motors() -> CommandListBuilder:
    """ Reset motors animation.

    :return: the animation command.
    """

    return command_list(
        motor(MotorId.lip_corners, 0.5, 0.0),
        motor(MotorId.eyebrows, 1.0, 0.0),
        motor(MotorId.eyelids, 0.0, 0.0),
        motor(MotorId.head_pitch, 0.5, 0.0),
        motor(MotorId.head_turn, 0.5, 0.0),
        motor(MotorId.mouth, 0.0, 0.0),
        wait_for_motors()
    )


def go_crazy() -> CommandListBuilder:
    """ Go crazy animation.

    :return: the animation command.
    """

    return command_list(
        motor(MotorId.head_turn, 0, 0.1),
        wait(0.8),

        motor(MotorId.head_turn, 1, 0.2),
        wait(0.8),

        motor(MotorId.head_turn, 0.5, 0.2),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.right_arm, 1, 0.5),
        wait_for_motors(),

        motor(MotorId.right_arm, 0, 0.5),
        wait_for_motors(),

        motor(MotorId.head_pitch, 1, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 1, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 1, 0.2),
        motor(MotorId.right_arm, 1, 0.5),
        wait_for_motors(),

        motor(MotorId.right_arm, 0, 0.5),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.7, 0.2),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.3, 0.2),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.7, 0.2),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.3, 0.2),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.7, 0.2),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.5, 0.2),
        motor(MotorId.right_arm, 1, 0.5),
        wait_for_motors(),

        motor(MotorId.right_arm, 0, 0.5),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        motor(MotorId.eyebrows, 0, 0.1),
        wait_for_motors(),

        motor(MotorId.head_turn, 0, 0.1),
        wait(0.4),

        motor(MotorId.head_pitch, 1, 0.2),
        motor(MotorId.head_turn, 1, 0.2),
        wait(0.7),

        motor(MotorId.head_turn, 0.5, 0.1),
        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.right_arm, 1, 0.1),
        motor(MotorId.mouth, 1.0, 0.3),
        wait(0.5),

        motor(MotorId.right_arm, 0, 2),
        motor(MotorId.mouth, 0.5, 2),
        motor(MotorId.mouth, 0, 2),
        motor(MotorId.eyebrows, 0, 2),
        motor(MotorId.head_pitch, 0.3, 2),
        wait(1),

        motor(MotorId.eyelids, 0.1, 0.5),
        wait_for_motors(),
        wait(1.5),
    )


def go_crazy2() -> CommandListBuilder:
    """ Go crazy variant 2 animation.

    :return: the animation command.
    """

    return command_list(
        motor(MotorId.eyelids, 1.0, 0.5),
        motor(MotorId.head_turn, 0.7, 0.5),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.3, 0.5),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.5, 0.5),
        motor(MotorId.head_turn, 0.1, 0.5),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.5),
        wait_for_motors()
    )


def go_crazy3() -> CommandListBuilder:
    """  Go crazy variant 3 animation.

    :return: the animation command.
    """

    return command_list(
        motor(MotorId.eyelids, 1, 0.5),
        wait(1.5),

        motor(MotorId.head_turn, 0, 0.1),
        wait(0.8),

        motor(MotorId.head_turn, 1, 0.2),
        wait(0.5),

        motor(MotorId.head_turn, 0.5, 0.2),
        wait_for_motors(),

        motor(MotorId.mouth, 0, 0.1),
        motor(MotorId.eyebrows, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.mouth, 1, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.5),
        wait_for_motors()
    )


def awkward() -> CommandListBuilder:
    """ Awkward animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.lip_corners, 0.7, 1.0),
        motor(MotorId.eyebrows, 0.3, 1.0),
        motor(MotorId.head_pitch, 1.0, 1.0),
        wait(0.6),

        motor(MotorId.eyelids, 1.0, 0.3),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.3),
        wait(0.3),

        motor(MotorId.lip_corners, 0.6, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.2, 0.5),
        motor(MotorId.eyebrows, 0.38, 0.5),
        motor(MotorId.eyelids, 0.43, 0.5),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.4, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.26, 0.2),
        motor(MotorId.eyebrows, 0.43, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.7, 0.7),
        motor(MotorId.eyebrows, 0.5, 0.7),
        motor(MotorId.eyelids, 0.0, 0.7),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.5, 1.0),
        motor(MotorId.head_pitch, 0.5, 1.0),
        wait_for_motors()
    )


def cute1() -> CommandListBuilder:
    """ Cute variant 1 animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.lip_corners, 0.37, 0.2),
        motor(MotorId.eyebrows, 1.0, 0.2),
        motor(MotorId.eyelids, 1.0, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.14, 0.2),
        motor(MotorId.eyelids, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.0, 0.2),
        wait(0.4),

        motor(MotorId.eyelids, 1.0, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.2),
        wait_for_motors(),
    )


def cute2() -> CommandListBuilder:
    """ Cute variant 2 animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.lip_corners, 0.37, 0.2),
        motor(MotorId.eyebrows, 1.0, 0.2),
        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.head_turn, 0.42, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.14, 0.2),
        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.head_turn, 0.31, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.05, 0.1),
        motor(MotorId.head_turn, 0.28, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.0, 0.1),
        motor(MotorId.head_pitch, 0.49, 0.1),
        motor(MotorId.head_turn, 0.28, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.41, 0.4),
        motor(MotorId.head_turn, 0.3, 0.4),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.head_pitch, 0.39, 0.2),
        motor(MotorId.head_turn, 0.31, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.head_pitch, 0.42, 0.2),
        motor(MotorId.head_turn, 0.32, 0.2),

        motor(MotorId.eyelids, 0.5, 0.1),
        motor(MotorId.head_pitch, 0.44, 0.1),
        motor(MotorId.head_turn, 0.33, 0.1),

        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.47, 0.1),
        motor(MotorId.head_turn, 0.32, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.head_pitch, 0.53, 0.2),
        motor(MotorId.head_turn, 0.31, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.62, 0.4),
        motor(MotorId.head_turn, 0.27, 0.4),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.61, 0.2),
        motor(MotorId.head_turn, 0.27, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.58, 0.3),
        motor(MotorId.head_turn, 0.31, 0.3),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.52, 0.5),
        motor(MotorId.head_turn, 0.45, 0.5),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.5, 0.3),
        motor(MotorId.head_turn, 0.5, 0.3),
        wait_for_motors(),
    )


def sleep() -> CommandListBuilder:
    """ Sleep animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.eyebrows, 1.0, 0.3),
        motor(MotorId.head_pitch, 0.8, 0.3),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.7, 0.2),
        wait(seconds=0.4),

        motor(MotorId.eyebrows, 0.5, 0.4),
        motor(MotorId.eyelids, 1.0, 0.4),
        motor(MotorId.head_pitch, 0.0, 0.4),
        wait_for_motors()
    )


def sleeping() -> CommandListBuilder:
    """ Sleeping animation.

    :return: the animation command.
    """

    return command_list(
        motor(MotorId.lip_corners, 0.5, 0.0),
        motor(MotorId.eyebrows, 0.5, 0.0),
        motor(MotorId.eyelids, 1.0, 0.0),
        motor(MotorId.head_pitch, 0.0, 0.0),
        motor(MotorId.head_turn, 0.5, 0.0),
        motor(MotorId.mouth, 0.0, 0.0),
        wait(seconds=0.7)
    )


def sleepy() -> CommandListBuilder:
    """ Sleepy animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.eyebrows, 1.0, 0.6),
        motor(MotorId.eyelids, 0.5, 0.6),
        motor(MotorId.head_pitch, 0.7, 0.6),
        motor(MotorId.mouth, 0.5, 0.6),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.57, 0.4),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.49, 0.2),
        motor(MotorId.mouth, 0.4, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.81, 0.3),
        motor(MotorId.eyelids, 0.64, 0.3),
        motor(MotorId.head_pitch, 0.4, 0.3),
        motor(MotorId.mouth, 0.11, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.74, 0.1),
        motor(MotorId.eyelids, 0.67, 0.1),
        motor(MotorId.head_pitch, 0.41, 0.1),
        motor(MotorId.mouth, 0.03, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.7, 0.1),
        motor(MotorId.head_pitch, 0.43, 0.1),
        motor(MotorId.mouth, 0.0, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.78, 0.2),
        motor(MotorId.head_pitch, 0.49, 0.2),
        motor(MotorId.mouth, 0.06, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 1.0, 0.4),
        motor(MotorId.eyelids, 0.43, 0.4),
        motor(MotorId.head_pitch, 0.6, 0.4),
        motor(MotorId.mouth, 0.37, 0.4),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.4, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.mouth, 0.43, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.4, 0.2),
        motor(MotorId.head_pitch, 0.65, 0.2),
        motor(MotorId.mouth, 0.5, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.41, 0.4),
        motor(MotorId.head_pitch, 0.72, 0.4),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.92, 0.1),
        motor(MotorId.eyelids, 0.42, 0.1),
        motor(MotorId.head_pitch, 0.72, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.76, 0.1),
        motor(MotorId.eyelids, 0.43, 0.1),
        motor(MotorId.head_pitch, 0.71, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.5, 0.2),
        motor(MotorId.eyelids, 0.5, 0.2),
        motor(MotorId.head_pitch, 0.65, 0.2),
        motor(MotorId.mouth, 0.25, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.head_pitch, 0.0, 0.2),
        motor(MotorId.mouth, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.58, 0.1),
        motor(MotorId.eyelids, 0.5, 0.1),
        motor(MotorId.head_pitch, 0.35, 0.1),
        motor(MotorId.mouth, 0.13, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.71, 0.1),
        motor(MotorId.eyebrows, 0.75, 0.1),
        motor(MotorId.eyelids, 0.0, 0.1),
        motor(MotorId.head_pitch, 0.7, 0.1),
        motor(MotorId.mouth, 0.36, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.8, 0.1),
        motor(MotorId.eyebrows, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.mouth, 0.5, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.55, 0.1),
        motor(MotorId.head_pitch, 0.65, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.99, 0.3),
        motor(MotorId.head_pitch, 0.64, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.98, 0.1),
        motor(MotorId.eyelids, 0.5, 0.1),
        motor(MotorId.head_pitch, 0.63, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.97, 0.1),
        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.head_turn, 0.54, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.94, 0.2),
        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.head_pitch, 0.61, 0.2),
        motor(MotorId.head_turn, 0.65, 0.2),
        motor(MotorId.mouth, 0.13, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.93, 0.1),
        motor(MotorId.head_pitch, 0.6, 0.1),
        motor(MotorId.mouth, 0.0, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.92, 0.1),
        motor(MotorId.head_pitch, 0.59, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.91, 0.1),
        motor(MotorId.head_pitch, 0.58, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.87, 0.3),
        motor(MotorId.head_pitch, 0.55, 0.3),
        motor(MotorId.head_turn, 0.4, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.81, 0.5),
        motor(MotorId.head_pitch, 0.51, 0.5),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.5, 0.2),
        motor(MotorId.eyebrows, 0.8, 0.2),
        motor(MotorId.head_pitch, 0.5, 0.2),
        motor(MotorId.head_turn, 0.5, 0.2),
        wait_for_motors(),
    )


def tell_a_joke() -> CommandListBuilder:
    """ Tell a joke animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.eyebrows, 1.0, 0.6),
        motor(MotorId.eyelids, 0.5, 0.6),
        motor(MotorId.head_pitch, 0.7, 0.6),
        motor(MotorId.mouth, 0.5, 0.6),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.57, 0.4),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.49, 0.2),
        motor(MotorId.mouth, 0.4, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.81, 0.3),
        motor(MotorId.eyelids, 0.64, 0.3),
        motor(MotorId.head_pitch, 0.4, 0.3),
        motor(MotorId.mouth, 0.11, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.74, 0.1),
        motor(MotorId.eyelids, 0.67, 0.1),
        motor(MotorId.head_pitch, 0.41, 0.1),
        motor(MotorId.mouth, 0.03, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.7, 0.1),
        motor(MotorId.head_pitch, 0.43, 0.1),
        motor(MotorId.mouth, 0.0, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.78, 0.2),
        motor(MotorId.head_pitch, 0.49, 0.2),
        motor(MotorId.mouth, 0.06, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 1.0, 0.4),
        motor(MotorId.eyelids, 0.43, 0.4),
        motor(MotorId.head_pitch, 0.6, 0.4),
        motor(MotorId.mouth, 0.37, 0.4),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.4, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.mouth, 0.43, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.4, 0.2),
        motor(MotorId.head_pitch, 0.65, 0.2),
        motor(MotorId.mouth, 0.5, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.41, 0.4),
        motor(MotorId.head_pitch, 0.72, 0.4),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.92, 0.1),
        motor(MotorId.eyelids, 0.42, 0.1),
        motor(MotorId.head_pitch, 0.72, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.76, 0.1),
        motor(MotorId.eyelids, 0.43, 0.1),
        motor(MotorId.head_pitch, 0.71, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.5, 0.2),
        motor(MotorId.eyelids, 0.5, 0.2),
        motor(MotorId.head_pitch, 0.65, 0.2),
        motor(MotorId.mouth, 0.25, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.head_pitch, 0.0, 0.2),
        motor(MotorId.mouth, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.58, 0.1),
        motor(MotorId.eyelids, 0.5, 0.1),
        motor(MotorId.head_pitch, 0.35, 0.1),
        motor(MotorId.mouth, 0.13, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.71, 0.1),
        motor(MotorId.eyebrows, 0.75, 0.1),
        motor(MotorId.eyelids, 0.0, 0.1),
        motor(MotorId.head_pitch, 0.7, 0.1),
        motor(MotorId.mouth, 0.36, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.8, 0.1),
        motor(MotorId.eyebrows, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.mouth, 0.5, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.55, 0.1),
        motor(MotorId.head_pitch, 0.65, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.99, 0.3),
        motor(MotorId.head_pitch, 0.64, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.98, 0.1),
        motor(MotorId.eyelids, 0.5, 0.1),
        motor(MotorId.head_pitch, 0.63, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.97, 0.1),
        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.head_turn, 0.54, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.94, 0.2),
        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.head_pitch, 0.61, 0.2),
        motor(MotorId.head_turn, 0.65, 0.2),
        motor(MotorId.mouth, 0.13, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.93, 0.1),
        motor(MotorId.head_pitch, 0.6, 0.1),
        motor(MotorId.mouth, 0.0, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.92, 0.1),
        motor(MotorId.head_pitch, 0.59, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.91, 0.1),
        motor(MotorId.head_pitch, 0.58, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.87, 0.3),
        motor(MotorId.head_pitch, 0.55, 0.3),
        motor(MotorId.head_turn, 0.4, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.81, 0.5),
        motor(MotorId.head_pitch, 0.51, 0.5),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.5, 0.2),
        motor(MotorId.eyebrows, 0.8, 0.2),
        motor(MotorId.head_pitch, 0.5, 0.2),
        motor(MotorId.head_turn, 0.5, 0.2),
        wait_for_motors()
    )


def wake_up() -> CommandListBuilder:
    """ Wake up animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),
        wait(seconds=0.9),

        motor(MotorId.eyebrows, 1.0, 0.5),
        motor(MotorId.eyelids, 1.0, 0.5),
        motor(MotorId.head_pitch, 0.2415, 0.5),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.5, 0.3),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.eyelids, 1.0, 0.04),
        wait_for_motors(),

        motor(MotorId.eyebrows, 1.0, 0.2),
        motor(MotorId.eyelids, 0.734, 0.16),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.465, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.555, 0.4),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.eyelids, 0.921, 0.1),
        motor(MotorId.head_pitch, 0.2415, 0.1),
        motor(MotorId.head_pitch, 0.508, 0.2),
        motor(MotorId.mouth, 0.0, 0.1),
        motor(MotorId.mouth, 0.51, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.748, 0.1),
        motor(MotorId.head_pitch, 0.5465, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.332, 0.2),
        motor(MotorId.head_pitch, 0.516, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.411, 0.2),
        motor(MotorId.head_pitch, 0.525, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.431, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.437, 0.3),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.446, 0.3),
        motor(MotorId.head_pitch, 0.4465, 0.3),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.583, 0.1),
        motor(MotorId.head_pitch, 0.439, 0.1),
        motor(MotorId.head_turn, 0.4775, 0.1),
        motor(MotorId.mouth, 0.446, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.988, 0.1),
        motor(MotorId.head_pitch, 0.499, 0.1),
        motor(MotorId.head_turn, 0.3735, 0.1),
        motor(MotorId.mouth, 0.215, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.eyelids, 0.635, 0.1),
        motor(MotorId.head_pitch, 0.629, 0.2),
        motor(MotorId.head_turn, 0.196, 0.2),
        motor(MotorId.mouth, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.135, 0.2),
        motor(MotorId.head_turn, 0.145, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.4675, 0.2),
        motor(MotorId.eyebrows, 0.82, 0.2),
        motor(MotorId.eyelids, 0.65, 0.2),
        motor(MotorId.head_pitch, 0.546, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.4035, 0.2),
        motor(MotorId.eyebrows, 0.63, 0.2),
        motor(MotorId.eyelids, 0.792, 0.16),
        motor(MotorId.eyelids, 0.724, 0.08),
        motor(MotorId.head_pitch, 0.496, 0.2),
        motor(MotorId.head_turn, 0.3395, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.334, 0.2),
        motor(MotorId.eyebrows, 0.512, 0.2),
        motor(MotorId.eyelids, 0.275, 0.16),
        motor(MotorId.head_pitch, 0.527, 0.2),
        motor(MotorId.head_turn, 0.642, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.294, 0.2),
        motor(MotorId.eyebrows, 0.56, 0.2),
        motor(MotorId.eyelids, 0.135, 0.2),
        motor(MotorId.head_pitch, 0.5585, 0.2),
        motor(MotorId.head_turn, 0.735, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.2255, 0.2),
        motor(MotorId.eyebrows, 0.774, 0.2),
        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.head_pitch, 0.613, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.172, 0.1),
        motor(MotorId.eyebrows, 0.935, 0.1),
        motor(MotorId.eyelids, 0.245, 0.1),
        motor(MotorId.head_pitch, 0.629, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.0, 0.7),
        motor(MotorId.eyebrows, 1.0, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.0, 0.2),
        motor(MotorId.eyelids, 0.707, 0.2),
        motor(MotorId.head_pitch, 0.652, 0.2),
        motor(MotorId.head_pitch, 0.652, 0.00333333333333),
        motor(MotorId.head_turn, 0.627, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.0, 0.3),
        motor(MotorId.eyelids, 1.0, 0.3),
        motor(MotorId.head_pitch, 0.5975, 0.296666666667),
        motor(MotorId.head_turn, 0.447, 0.3),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.57, 0.2),
        motor(MotorId.head_turn, 0.4385, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.5385, 0.3),
        motor(MotorId.head_turn, 0.409, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.971, 0.3),
        motor(MotorId.head_pitch, 0.507, 0.3),
        motor(MotorId.head_turn, 0.3815, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.821, 0.3),
        motor(MotorId.head_pitch, 0.5485, 0.3),
        motor(MotorId.head_turn, 0.372, 0.3),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.512, 0.7),
        motor(MotorId.eyelids, 0.135, 0.7),
        motor(MotorId.head_pitch, 0.5225, 0.7),
        motor(MotorId.head_turn, 0.449, 0.7),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.5015, 0.6),
        motor(MotorId.head_turn, 0.543, 0.6),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0., 0.3),
        motor(MotorId.head_pitch, 0.492, 0.3),
        motor(MotorId.head_turn, 0.563, 0.3),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.05, 0.8),
        motor(MotorId.head_pitch, 0.4455, 0.8),
        motor(MotorId.head_turn, 0.457, 0.8),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.115, 0.2),
        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.head_pitch, 0.454, 0.2),
        motor(MotorId.head_turn, 0.419, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.166, 0.3),
        motor(MotorId.eyelids, 0.327, 0.3),
        motor(MotorId.head_pitch, 0.471, 0.3),
        motor(MotorId.head_turn, 0.402, 0.3),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.1805, 0.1),
        motor(MotorId.eyelids, 0.114, 0.1),
        motor(MotorId.head_pitch, 0.4765, 0.1),
        motor(MotorId.head_turn, 0.4025, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.2875, 0.7),
        motor(MotorId.eyelids, 0.121, 0.7),
        motor(MotorId.head_pitch, 0.52, 0.7),
        motor(MotorId.head_turn, 0.4655, 0.7),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.135, 1.0),
        motor(MotorId.head_pitch, 0.4905, 1.0),
        motor(MotorId.head_turn, 0.548, 1.0),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.135, 0.1),
        motor(MotorId.head_pitch, 0.4855, 0.1),
        motor(MotorId.head_turn, 0.547, 0.1),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.3),
        motor(MotorId.head_pitch, 0.4735, 0.3),
        motor(MotorId.head_turn, 0.5375, 0.3),
        wait_for_motors(),

        motor(MotorId.eyelids, 0.114, 0.3),
        motor(MotorId.head_pitch, 0.459, 0.3),
        motor(MotorId.head_turn, 0.524, 0.3),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.4345, 0.6),
        motor(MotorId.head_turn, 0.506, 0.6),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.4295, 0.3),
        motor(MotorId.head_turn, 0.504, 0.3),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.568, 1.1),
        motor(MotorId.head_turn, 0.469, 1.1),
        wait_for_motors(),

        motor(MotorId.head_turn, 0.4435, 1.3),
        wait_for_motors()
    )


def worry() -> CommandListBuilder:
    """ Worry animation.

    :return: the animation command.
    """

    return command_list(
        reset_motors(),

        motor(MotorId.eyebrows, 0.05, 0.2),
        motor(MotorId.eyelids, 0.74, 0.2),
        motor(MotorId.head_pitch, 0.28, 0.2),
        motor(MotorId.head_turn, 0.68, 0.2),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.3, 0.1),
        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.2, 0.1),
        motor(MotorId.head_turn, 0.58, 0.1),
        motor(MotorId.mouth, 0.26, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 1.0, 0.2),
        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.head_pitch, 1.0, 0.2),
        motor(MotorId.head_turn, 0.29, 0.2),
        motor(MotorId.mouth, 1.0, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.86, 0.2),
        motor(MotorId.eyebrows, 0.0, 0.2),
        motor(MotorId.eyelids, 0.5, 0.2),
        motor(MotorId.head_pitch, 0.98, 0.2),
        motor(MotorId.head_turn, 0.0, 0.2),
        motor(MotorId.mouth, 0.0, 0.2),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.94, 0.1),
        motor(MotorId.head_turn, 0.5, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.9, 0.1),
        motor(MotorId.head_turn, 1.0, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.86, 0.1),
        motor(MotorId.head_turn, 0.5, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.82, 0.1),
        motor(MotorId.head_turn, 0.0, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.78, 0.1),
        motor(MotorId.head_turn, 0.43, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.74, 0.1),
        motor(MotorId.head_turn, 0.87, 0.1),
        wait_for_motors(),

        motor(MotorId.head_pitch, 0.66, 0.2),
        motor(MotorId.head_turn, 0.29, 0.2),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.73, 0.1),
        motor(MotorId.head_pitch, 0.62, 0.1),
        motor(MotorId.head_turn, 0.31, 0.1),
        wait_for_motors(),

        motor(MotorId.lip_corners, 0.6, 0.1),
        motor(MotorId.eyebrows, 0.08, 0.1),
        motor(MotorId.eyelids, 0.75, 0.1),
        motor(MotorId.head_pitch, 0.58, 0.1),
        motor(MotorId.head_turn, 0.36, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.24, 0.1),
        motor(MotorId.eyelids, 1.0, 0.1),
        motor(MotorId.head_pitch, 0.55, 0.1),
        motor(MotorId.head_turn, 0.42, 0.1),
        wait_for_motors(),

        motor(MotorId.eyebrows, 0.5, 0.2),
        motor(MotorId.eyelids, 0.2, 0.2),
        motor(MotorId.head_pitch, 0.5, 0.2),
        motor(MotorId.head_turn, 0.5, 0.2),
        wait_for_motors(),

        motor(MotorId.eyelids, 1.0, 0.2),
        motor(MotorId.eyelids, 0.0, 0.2),
        motor(MotorId.eyelids, 0.2, 0.2),
        wait_for_motors()
    )
