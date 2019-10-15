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

import socket
import sys
import threading
from typing import Callable

import logbook
from logbook import Logger, StreamHandler


class TcpTransport:
    """ Creates a TCP connection to the robot, enabling commands to be sent to and from the robot. """

    def __init__(self, tcp_ip: str = '192.168.1.1', tcp_port: int = 8080, buffer_size: int = 4096,
                 initial_timeout: float = 5.0, data_received_cb: Callable[[str], None] = None, encoding: str = 'utf-8',
                 initial_cmd: str = '', log_level=logbook.INFO):
        """ Constructor for TcpTransport, which is used to send and receive data to and from the robot respectively.

        :param tcp_ip: IP address of robot.
        :param tcp_port: port of robot.
        :param buffer_size: the size of the TCP read buffer.
        :param initial_timeout: how long to wait when connecting to the robot's socket.
        :param data_received_cb: a callback function to receive data back from the robot with.
        :param encoding: encoding to send data over socket in.
        :param initial_cmd: the first command to send.
        :param log_level: the level for displaying and logging information, e.g. debugging information.
        """

        StreamHandler(sys.stdout).push_application()
        self._log = Logger('TcpTransport')
        self._log.level = log_level
        self._tcp_ip = tcp_ip
        self._tcp_port = tcp_port
        self._data_received_cb = data_received_cb
        self._encoding = encoding
        self._lock = threading.Lock()
        self._buffer_size = buffer_size
        self._initial_timeout = initial_timeout
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._initial_cmd = initial_cmd
        self._is_read_thread_running = False
        self._read_thread = None

    def close(self) -> None:
        """ Close the connection to the robot and shut down the reading thread.

        :return: None.
        """

        self._is_read_thread_running = False
        self._sock.close()
        if self._read_thread is not None:
            self._read_thread.join()

    def send(self, message: str) -> None:
        """ Send a message to the robot.

        :param message: the message to send to the robot.
        :return: None.
        """

        with self._lock:
            try:
                self._sock.sendall(message.encode(self._encoding))
            except socket.error as e:
                self._log.error("Error sending message to socket: {}".format(e))

    def connect(self) -> bool:
        """ Connects to the robot's TCP socket endpoint.

        :return: whether the connection was successful or not.
        """

        try:
            self._log.debug("Connecting to socket: tcp_ip={}, tcp_port={}".format(self._tcp_ip, self._tcp_port))
            self._sock.settimeout(self._initial_timeout)
            self._sock.connect((self._tcp_ip, self._tcp_port))
            self._sock.settimeout(None)
            self.send(self._initial_cmd)
            self._init_read_thread()
            self._log.debug("Socket connected")
            return True
        except socket.error as e:
            self._log.error("Error connecting to socket: {}".format(e))
            return False

    def _init_read_thread(self) -> None:
        """ Initialize the thread for reading data from the robot.

        :return: None.
        """

        if not self._is_read_thread_running:
            self._is_read_thread_running = True
            self._read_thread = threading.Thread(target=self._read_thread_func)
            self._read_thread.start()

    def _read_thread_func(self) -> None:
        """ The function run by the read thread; it reads data from the robot and sends data elsewhere via a user
        supplied callback.

        :return: None.
        """

        while self._is_read_thread_running:
            try:
                data = self._sock.recv(self._buffer_size)
                if data:
                    self._log.debug("Data read from socket: {}".format(str(data)))
                    # If we have data and a callback is registered then fire off the callback
                    if self._data_received_cb:
                        self._data_received_cb(data.decode(self._encoding))
            except socket.error as e:
                # Errors when closing the socket are expected, i.e. when the read thread has been stopped
                if self._is_read_thread_running:
                    self._log.error("Error reading data from socket: {}".format(e))
