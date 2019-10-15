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

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List


class CallbackType(Enum):
    """ The type of callback command. """

    start = 'TS'
    end = 'TE'


class WaitType(Enum):
    """ The type of wait command. """

    wait_for_motors = auto()
    wait_for_motors_and_speaking = auto()
    wait = auto()
    wait_for_say_start = auto()
    wait_for_say_done = auto()


class WalkDirection(Enum):
    """ The directions the robot can walk. """

    forward = auto()
    backward = auto()
    left = auto()
    right = auto()


class MotorId(Enum):
    """ The ids of the robot's motors. """

    right_arm = 'AR'
    lip_corners = 'CH'
    eyebrows = 'EB'
    eyelids = 'EL'
    head_pitch = 'HN'
    head_turn = 'HT'
    mouth = 'MO'


class CommandBuilder(ABC):
    """ Abstract CommandBuilder interface. CommandBuilders are used to generate the actions the robot can perform. """

    @abstractmethod
    def duration(self) -> float:
        """ Implement, calculates the duration in seconds that the command will take to execute on the robot.

        :return: duration in seconds.
        """

        raise NotImplementedError("Please implement the `duration` method")

    @abstractmethod
    def build(self) -> str:
        """ Implement, builds a string command that makes the robot perform an action.

        :return: a string command.
        """

        raise NotImplementedError("Please implement the `build` method")


class WaitCommandBuilder(CommandBuilder):
    """ WaitCommandBuilder  """

    __COMMANDS = {WaitType.wait_for_motors: "<PM>",
                  WaitType.wait_for_motors_and_speaking: "<PA>",
                  WaitType.wait: "<PA={}>",
                  WaitType.wait_for_say_start: "<SS>",
                  WaitType.wait_for_say_done: "<PS>"}

    def __init__(self, wait_type: WaitType, seconds: float = 0.):
        CommandBuilder.__init__(self)
        self.wait_type = wait_type
        self.seconds = seconds

    def duration(self) -> float:
        return self.seconds

    def build(self) -> str:
        if self.wait_type is WaitType.wait:
            return WaitCommandBuilder.__COMMANDS[self.wait_type].format(self.seconds)
        return WaitCommandBuilder.__COMMANDS[self.wait_type]


class CallbackCommandBuilder(CommandBuilder):
    """ Builds a command that triggers a callback when certain commands have started or finished. """

    def __init__(self, callback_type: CallbackType, callback_id: str):
        """ Constructor for CallbackCommandBuilder.

        :param callback_type: the type of callback to be triggered, either at the start of a command or the end.
        :param callback_id: the string id to give the callback.
        """

        CommandBuilder.__init__(self)
        self.callback_type = callback_type
        self.callback_id = callback_id

    def duration(self) -> float:
        return 0

    def build(self) -> str:
        return "<{}={}>".format(self.callback_type.value, self.callback_id)


class CommandListBuilder(CommandBuilder):
    """ Builds a list of commands by concatenating them together """

    def __init__(self, commands: List[CommandBuilder]):
        """ Constructor for CommandListBuilder.

        :param commands: the list of commands to concatenate together.
        """

        CommandBuilder.__init__(self)
        self.commands = commands

    def duration(self) -> float:
        return 0

    def build(self) -> str:
        str_commands = []
        for cmd in self.commands:
            str_commands.append(cmd.build())
        command = ''.join(str_commands)
        return command


class WalkCommandBuilder(CommandBuilder):
    """ Builds commands that make the robot walk. """

    __STEP_TIMES = {WalkDirection.forward: 2.3,
                    WalkDirection.backward: 2.4,
                    WalkDirection.left: 1.1,
                    WalkDirection.right: 1.1}

    __COMMANDS = {WalkDirection.forward: "<WK=W2,{}>",
                  WalkDirection.backward: "<WK=WB,{}>",
                  WalkDirection.left: "<WK=WL,{}>",
                  WalkDirection.right: "<WK=WR,{}>"}

    def __init__(self, direction: WalkDirection, steps: int = 4):
        """ Constructor for WalkCommandBuilder.

        :param direction: the direction to walk, one of forward, backward, left or right.
        :param steps: the number of steps to take. Must be between 1 and 10 steps. For forward and backward, a step
        means both feet step forward one time each. For left and right a step means that the foot in question moves
        the number of times given by the step parameter.
        """

        if not (0 < steps < 11):
            raise ValueError(
                'WalkCommandBuilder.__init__ expected steps to be between 1 and 10, however received {}'.format(steps))

        CommandBuilder.__init__(self)
        self.steps = steps
        self.direction = direction

    def duration(self) -> float:
        return WalkCommandBuilder.__STEP_TIMES[self.direction] * self.steps

    def build(self) -> str:
        steps = self.steps
        if self.steps == 1:
            steps = 0
        cmd = WalkCommandBuilder.__COMMANDS[self.direction].format(steps, self.duration())
        return cmd


class MotorCommandBuilder(CommandBuilder):
    """ Builds commands to move the robot's motors. """

    def __init__(self, motor_id: MotorId, position: float, seconds: float):
        """ Constructor for MotorCommandBuilder.

        :param motor_id: the ID of the motor.
        :param position: the position to move the motor to, between 0.0 and 1.0.
        :param seconds: the time in seconds that the motor should take to move to the desired position, between 0.0 and
        10.0.
        """

        if not (0. <= position <= 1.):
            raise ValueError(
                "MotorCommandBuilder.__init__ expected 'position' to be between "
                "0.0 and 1.0, however received '{}'".format(position))

        if not (0. <= seconds <= 10.):
            raise ValueError(
                "MotorCommandBuilder.__init__ expected 'seconds' to be between "
                "0.0 and 10.0, however received '{}'".format(seconds))

        CommandBuilder.__init__(self)
        self.motor_id = motor_id
        self.position = position
        self.seconds = seconds

    def duration(self) -> float:
        return self.seconds

    def build(self) -> str:
        cmd = "<MO={motor_id},{position:.1f},{time:.1f}>".format(motor_id=self.motor_id.value, position=self.position,
                                                                 time=self.seconds)
        return cmd


class SayCommandBuilder(CommandBuilder):
    """ Builds commands to make the robot speak. """

    def __init__(self, text: str, wpm: int = 112):
        """ Constructor for SayCommandBuilder.

        :param text: the text for the robot to speak.
        :param wpm: the estimated words per minute that the robot speaks at. This does not modify the speed that the
        robot speaks at, just the estimate of how long it will speak for. The default value of 112 is the estimated
        WPM for the Professor Einstein text to speech engine.
        """

        if wpm <= 0:
            raise ValueError(
                "SayCommandBuilder.__init__ expected 'wpm' to be greater than 0, however received '{}'".format(wpm))

        CommandBuilder.__init__(self)
        self.text = text
        self.wpm = wpm

    def duration(self) -> float:
        num_words = len(self.text.split(' '))
        seconds = num_words / self.wpm * 60.
        return seconds

    def build(self) -> str:
        return self.text
