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

import json
import sys
import threading
import time
from enum import Enum, auto
from typing import Callable

import logbook
from logbook import Logger, StreamHandler

from hr_little_api.functional import *
from hr_little_api.json_api import generate_id, activity_cmd, voltage_cmd
from hr_little_api.transport import TcpTransport


class Animation(Enum):
    """ Types of pre-made animations the robot can play """

    right_arm_down = auto()
    right_arm_point = auto()
    head_down = auto()
    head_middle = auto()
    head_up = auto()
    head_turn_left = auto()
    head_turn_middle = auto()
    head_turn_right = auto()
    close_mouth = auto()
    open_mouth = auto()
    poke_tounge = auto()
    eye_lid_open = auto()
    eye_lid_close = auto()
    raise_eyebrows = auto()
    frown_eyebrows = auto()
    smile = auto()
    mouth_neutral = auto()
    mouth_frown = auto()
    reset = auto()
    go_crazy = auto()
    go_crazy2 = auto()
    go_crazy3 = auto()
    awkward = auto()
    cute1 = auto()
    cute2 = auto()
    sleep = auto()
    sleeping = auto()
    sleepy = auto()
    tell_a_joke = auto()
    wake_up = auto()
    worry = auto()


class ActionHandle:
    """ Provides functionality for waiting until an action has completed, signaling when an action has completed
    and triggering and sending a callback when an action has finished.
    """

    def __init__(self, timeout: float = None, log_level=logbook.INFO):
        """ ActionHandle constructor.

        :param timeout: the timeout in seconds for the action handle to wait before it considers the action has
        completed. This is for handling actions on the robot that don't support triggers.
        :param log_level: the level for displaying and logging information, e.g. debugging information.
        """

        StreamHandler(sys.stdout).push_application()
        self._log = Logger('Robot')
        self._log.level = log_level

        self.id = generate_id()
        self.callbacks = []
        self.timeout = timeout
        self.event_ = threading.Event()
        if self.timeout is not None:
            self.timer_ = threading.Timer(self.timeout, self.done)

    def add_callback(self, done_cb: Callable[[], None] = None) -> None:
        """ Add a callback function to the action handle, which will be triggered when the action has finished.

        :param done_cb: the function to call.
        :return: None.
        """

        if done_cb is not None:
            self.callbacks.append(done_cb)

    def start_timer(self) -> None:
        """ Start the timer to trigger the completion of the action handle after a 'timeout', which is given
        in the constructor. Used when a robot action doesn't have a mechanism to notify when it has completed.

        :return: None.
        """

        if self.timeout is not None:
            self.timer_.start()
        else:
            self._log.warn("ActionHandle.start_timer: the 'timeout' parameter of ActionHandle is not set, "
                           "it needs to be set before starting the action handle in timer mode")

    def wait(self) -> None:
        """ Block and wait until the action has completed.

        :return: None.
        """

        self.event_.wait()

    def done(self) -> None:
        """ Informs that action handle that the action has finished and calls the 'done_cb' function if it has been set.
        Called by self.timer_ or in the Robot._update_state method.

        :return: None.
        """

        self.event_.set()
        for cb in self.callbacks:
            cb()


class Robot:
    """ The Robot class enables you to connect to the robot, send actions and read data from the robot.

    :var version: the version of the robot's firmware.
    :var voltage: the voltage of the robot's batteries, between 0.0 and 1.0.
    :var is_connected: whether the robot has connected or not.

    """

    __animation_map = {Animation.right_arm_down: right_arm_down, Animation.right_arm_point: right_arm_point,
                       Animation.head_down: head_down, Animation.head_middle: head_middle, Animation.head_up: head_up,
                       Animation.head_turn_left: head_turn_left, Animation.head_turn_middle: head_turn_middle,
                       Animation.head_turn_right: head_turn_right, Animation.close_mouth: close_mouth,
                       Animation.open_mouth: open_mouth, Animation.poke_tounge: poke_tounge,
                       Animation.eye_lid_open: eye_lid_open, Animation.eye_lid_close: eye_lid_close,
                       Animation.raise_eyebrows: raise_eyebrows, Animation.frown_eyebrows: frown_eyebrows,
                       Animation.smile: smile, Animation.mouth_neutral: mouth_neutral,
                       Animation.mouth_frown: mouth_frown, Animation.reset: reset_motors, Animation.go_crazy: go_crazy,
                       Animation.go_crazy2: go_crazy2, Animation.go_crazy3: go_crazy3, Animation.awkward: awkward,
                       Animation.cute1: cute1, Animation.cute2: cute2, Animation.sleep: sleep,
                       Animation.sleeping: sleeping, Animation.sleepy: sleepy, Animation.tell_a_joke: tell_a_joke,
                       Animation.wake_up: wake_up, Animation.worry: worry}

    def __init__(self, read_rate_hz: float = 0.05, log_level=logbook.INFO):
        """ The Robot constructor.

        :param read_rate_hz: the rate in Hz to read data from the robot.
        :param log_level: the level for displaying and logging information, e.g. debugging information.
        """

        StreamHandler(sys.stdout).push_application()
        self.version: str = ""
        self.voltage: float = float("NaN")
        self.is_connected: bool = False
        self._log = Logger('Robot')
        self._log.level = log_level
        self._read_rate_hz = read_rate_hz
        self._keep_alive_secs = 9.0
        self._read_commands = [voltage_cmd()]
        self._read_thread = threading.Thread(target=self._send_read_cmds)
        self._read_event = threading.Event()
        self._keep_alive_thread = threading.Thread(target=self._keep_alive)
        self._keep_alive_event = threading.Event()
        self._transport = TcpTransport(data_received_cb=self._data_received_cb,
                                       initial_cmd=activity_cmd(" "),
                                       log_level=log_level)
        self._action_handle_lock = threading.Lock()
        self._action_handles = {}
        self._is_action_active_lock = threading.Lock()
        self._is_action_active = False
        self._is_running = False
        self._last_cmd_time = 0

    def connect(self) -> bool:
        """ Creates a network connection with the robot, i.e. a TCP socket stream. This method must be called
        before controlling the robot.

        :return: whether the connection was successful or not.
        """

        self._log.info("Connecting to robot...")
        self.is_connected = self._transport.connect()

        if self.is_connected:
            self.animate(Animation.eye_lid_open)  # the animation that plays right after Einstein connects gets stopped
            # just as he is closing his eyes

            self._is_running = True
            self._read_thread.start()
            time.sleep(1)

            self._last_cmd_time = time.time()
            self._keep_alive_thread.start()
            time.sleep(2)

            self._log.info("Connected.")

        return self.is_connected

    def disconnect(self) -> None:
        """ Close the network connection with the robot. This method must be called before the program finishes.

        :return: None.
        """
        self._log.info("Disconnecting from robot...")
        self._is_running = False
        self._transport.close()

        self._read_event.set()
        if self._read_thread.is_alive():
            self._read_thread.join()
        self._keep_alive_event.set()  # Will cancel keep alive from sleeping
        if self._keep_alive_thread.is_alive():
            self._keep_alive_thread.join()
        self._log.info("Disconnected.")

    def say(self, text: str, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        """ An action to make the robot speak.

        :param text: the text for the robot to speak.
        :param block: whether to block until the action has finished.
        :param done_cb: a callback to be triggered when the action has completed.
        :return: an action handle.
        """
        self._set_action_start()
        builder = say(text)
        handle = ActionHandle()
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        self._add_action_handle(handle)
        cmd = activity_cmd(builder.build() + callback_end(handle.id).build())
        self._transport.send(cmd)

        if block:
            self.wait(handle)

        return handle

    def walk_forward(self, steps: int = 4, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        """ An action to make the robot walk forward a given number of steps.

        :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means both feet step
        forward once time each.
        :param block: whether to block until the action has finished.
        :param done_cb: a callback to be triggered when the action has completed.
        :return: an action handle.
        """
        self._set_action_start()
        builder = walk_forward(steps=steps)
        handle = ActionHandle(timeout=builder.duration())
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        cmd = activity_cmd(builder.build())
        self._transport.send(cmd)
        handle.start_timer()

        if block:
            self.wait(handle)

        return handle

    def walk_backward(self, steps: int = 4, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        """ An action to make the robot walk backward a given number of steps.

        :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means both feet step
        backward once time each.
        :param block: whether to block until the action has finished.
        :param done_cb: a callback to be triggered when the action has completed.
        :return: an action handle.
        """
        self._set_action_start()
        builder = walk_backward(steps=steps)
        handle = ActionHandle(timeout=builder.duration())
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        cmd = activity_cmd(builder.build())
        self._transport.send(cmd)
        handle.start_timer()

        if block:
            self.wait(handle)

        return handle

    def walk_left(self, steps: int = 4, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        """ An action to make the robot walk left a given number of steps.

        :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means the right foot takes
        a single step, making the robot walk left.
        :param block: whether to block until the action has finished.
        :param done_cb: a callback to be triggered when the action has completed.
        :return: an action handle.
        """
        self._set_action_start()
        builder = walk_left(steps=steps)
        handle = ActionHandle(timeout=builder.duration())
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        cmd = activity_cmd(builder.build())
        self._transport.send(cmd)
        handle.start_timer()

        if block:
            self.wait(handle)

        return handle

    def walk_right(self, steps: int = 4, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        """ An action to make the robot walk right a given number of steps.

        :param steps: the number of steps to take. Must be between 1 and 10 steps. A step means the left foot takes
        a single step, making the robot walk right.
        :param block: whether to block until the action has finished.
        :param done_cb: a callback to be triggered when the action has completed.
        :return: an action handle.
        """
        self._set_action_start()
        builder = walk_right(steps=steps)
        handle = ActionHandle(timeout=builder.duration())
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        cmd = activity_cmd(builder.build())
        self._transport.send(cmd)
        handle.start_timer()

        if block:
            self.wait(handle)

        return handle

    def animate(self, animation: Animation, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        """ An action to make the robot perform an animation.

        :param animation: the type of animation to perform.
        :param block: whether to block until the action has finished.
        :param done_cb: a callback to be triggered when the action has completed.
        :return: an action handle.
        """
        self._set_action_start()
        builder = self.__animation_map[animation]()
        handle = ActionHandle()
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        self._add_action_handle(handle)
        # For the TE callback fire after motors, you *need a space* and then the <PA> command before <TE=...>
        # this forces the TE command to wait until after the robot has spoken the space.
        cmd = activity_cmd(
            builder.build() + " " + wait_for_motors_and_speaking().build() + callback_end(handle.id).build())
        self._transport.send(cmd)

        if block:
            self.wait(handle)

        return handle

    def do(self, *commands, block: bool = True, done_cb: Callable[[], None] = None) -> ActionHandle:
        self._set_action_start()
        cmd_list = [cmd for cmd in commands]
        builder = command_list(*cmd_list)
        handle = ActionHandle()
        handle.add_callback(done_cb)
        handle.add_callback(self._set_action_done)
        self._add_action_handle(handle)
        # For the TE callback fire after motors, you *need a space* and then the <PA> command before <TE=...>
        # this forces the TE command to wait until after the robot has spoken the space.
        cmd = activity_cmd(
            builder.build() + " " + wait_for_motors_and_speaking().build() + callback_end(handle.id).build())
        self._transport.send(cmd)

        if block:
            self.wait(handle)

        return handle

    def wait(self, *action_handles) -> None:
        """ Block until the given action handles have finished.

        :param action_handles:
        :return: None.
        """

        for handle in action_handles:
            handle.wait()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def _set_action_start(self):
        with self._is_action_active_lock:
            self._is_action_active = True

    def _set_action_done(self):
        with self._is_action_active_lock:
            self._last_cmd_time = time.time()
            self._is_action_active = False

    def _add_action_handle(self, handle: ActionHandle) -> None:
        with self._action_handle_lock:
            self._action_handles[handle.id] = (0, handle)

    def _set_action_handle_done(self, action_id: str) -> None:
        handle_to_finish = None

        with self._action_handle_lock:
            if action_id in self._action_handles:
                # These get triggered twice because the robot sends two triggers back
                # for some reason. We send the callback on the second trigger in case
                # it affects the behaviour.
                count, ah = self._action_handles[action_id]
                count += 1

                if count > 1:
                    self._action_handles.pop(action_id)
                    handle_to_finish = ah
                else:
                    self._action_handles[action_id] = (count, ah)
            else:
                self._log.warn(
                    "Robot._set_action_handle_done: ActionHandle with action_id '{}' not found".format(action_id))

        if handle_to_finish is not None:
            handle_to_finish.done()

    def _send_read_cmds(self):
        while self._is_running:
            for cmd in self._read_commands:
                self._transport.send(cmd)
            secs = 1. / self._read_rate_hz
            self._read_event.wait(timeout=secs)

    def _keep_alive(self):
        """ This function makes sure that the robot doesn't say or do it's automatic functions whilst we
        are using it, because it interferes with the programs we want to write. This function is called
        every 9 seconds and only sends a command to the robot if an action isn't currently running
        and the last command was sent 9 seconds ago. """
        while self._is_running:
            secs_since_last_cmd = time.time() - self._last_cmd_time
            if not self._is_action_active and secs_since_last_cmd > self._keep_alive_secs:
                self._transport.send(activity_cmd(" "))
                self._last_cmd_time = time.time()
                self._log.debug("Keeping alive")
            self._keep_alive_event.wait(timeout=self._keep_alive_secs)

    def _data_received_cb(self, msg):
        self._log.debug("data_received_cb: {}".format(msg))
        # TODO: handle partial messages

        try:
            # Parse messages, there can be more than one json message returned in msg
            prev_index = 0
            msg_len = len(msg)

            while prev_index < msg_len:
                start_index = prev_index + msg[prev_index:].find('{')
                sub_msg_len = int(msg[prev_index:start_index])
                end_index = start_index + sub_msg_len
                sub_msg = msg[start_index:end_index]
                data = json.loads(sub_msg)
                # When each message has been parsed into json, update the robots state
                self._update_state(data)
                prev_index = end_index
        except ValueError as e:
            self._log.error("Error decoding json for message: {}. Error: {}".format(msg, e))

    def _update_state(self, data):
        if "device" in data and self.version is '':
            self.version = data["device"]["version"]

        if "trigger" in data:
            trigger = data["trigger"]

            if trigger.startswith("voltage."):
                self.voltage = float(trigger.replace("voltage.", "")) / 10.
            elif trigger.startswith("cb."):
                self._log.debug("Trigger received: {}".format(trigger))
                self._set_action_handle_done(trigger)
            else:
                self._log.debug("Unknown trigger: {}".format(trigger))
