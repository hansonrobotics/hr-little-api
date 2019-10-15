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

import uuid


def generate_id() -> str:
    """ Generate a unique string id which can be used for the TS and TE commands.

    :return: a unique id.
    """

    # The TS and TE command string parameter needs to be under N characters (should figure out what N is, but
    # 25 characters has been tested to work).
    return "cb." + str(uuid.uuid1()).replace('-', '')[:-10]


def json_length(msg_body: str) -> str:
    """ The robot's JSON API requires the length of the JSON command to be specified before the JSON command. This
    function calculates the length of the JSON message body and formats it for the JSON API.

    :param msg_body: the JSON message body.
    :return: the length of the JSON message.
    """

    length = len(msg_body)

    if length > 4090:
        raise ValueError(
            'The maximum message length for the JSON API is 4090, however the length is {}'.format(length))

    return str(length).zfill(6)


def echo_cmd() -> str:
    """ Make the echo command, which send a message to the robot which it sends back.

    :return: the command.
    """

    msg_body = '{"cmd":"echo"}'
    return json_length(msg_body) + msg_body


def push_ping_cmd() -> str:
    """

    :return:
    """

    msg_body = '{"cmd":"pushping"}'
    return json_length(msg_body) + msg_body


def voltage_cmd() -> str:
    """ Make the voltage command, which returns the voltage of the robot's batteries between 0 to 10.

    :return: the command.
    """
    msg_body = '{"cmd":"voltage"}'
    return json_length(msg_body) + msg_body


def switch_to_ble_cmd() -> str:
    """ Make the switch to ble command, which switches the robot from bluetooth low energy mode to WiFi mode.

    :return: the command.
    """

    msg_body = '{"cmd":"switch_to_ble"}'
    return json_length(msg_body) + msg_body


def activity_cmd(cmd: str) -> str:
    """ Make the activity command, which enables one to send motor, walking and text to speech scripts to the robot.

    :param cmd: the motor, walking or text to speech sub commands.
    :return: the command.
    """

    msg_body = '{"cmd":"activity.recieved","data":{"output":"' + cmd + '"}}'
    return json_length(msg_body) + msg_body
