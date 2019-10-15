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

import unittest

from hr_little_api.builders import CommandBuilder, SayCommandBuilder, WalkCommandBuilder, WalkDirection, \
    MotorCommandBuilder, MotorId


class TestCommandBuilder(unittest.TestCase):
    def test_abstract(self):
        with self.assertRaises(TypeError):
            CommandBuilder()


class TestSayCommandBuilder(unittest.TestCase):

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            SayCommandBuilder('Hello', wpm=0)

    def test_duration(self):
        builder = SayCommandBuilder('Hello world I am Professor Einstein', wpm=100)
        expected_duration = 3.6
        self.assertAlmostEqual(expected_duration, builder.duration())

    def test_build(self):
        text = 'hello world'
        builder = SayCommandBuilder(text)
        actual_cmd = builder.build()
        self.assertEqual(text, actual_cmd)


class TestWalkCommandBuilder(unittest.TestCase):
    def test_invalid_range(self):
        # Test invalid walk commands: 0, i.e. less than 1
        with self.assertRaises(ValueError):
            WalkCommandBuilder(WalkDirection.forward, steps=0)

        # Test invalid walk commands: 11, i.e. greater than 10
        with self.assertRaises(ValueError):
            WalkCommandBuilder(WalkDirection.forward, steps=11)

    def test_walk_forward(self):
        # Test all valid walk forward commands
        expected_cmds = ["<WK=W2,0>"] + ["<WK=W2,{}>".format(i) for i in range(2, 10)]
        for i in range(1, 10):
            builder = WalkCommandBuilder(WalkDirection.forward, steps=i)
            actual_cmd = builder.build()
            expected_cmd = expected_cmds[i - 1]
            self.assertEqual(expected_cmd, actual_cmd)

    def test_walk_backward(self):
        # Test all valid walk backward commands
        expected_cmds = ["<WK=WB,0>"] + ["<WK=WB,{}>".format(i) for i in range(2, 10)]
        for i in range(1, 10):
            builder = WalkCommandBuilder(WalkDirection.backward, steps=i)
            actual_cmd = builder.build()
            expected_cmd = expected_cmds[i - 1]
            self.assertEqual(expected_cmd, actual_cmd)

    def test_walk_left(self):
        # Test all valid walk left commands
        expected_cmds = ["<WK=WL,0>"] + ["<WK=WL,{}>".format(i) for i in range(2, 10)]
        for i in range(1, 10):
            builder = WalkCommandBuilder(WalkDirection.left, steps=i)
            actual_cmd = builder.build()
            expected_cmd = expected_cmds[i - 1]
            self.assertEqual(expected_cmd, actual_cmd)

    def test_walk_right(self):
        # Test all valid walk right commands
        expected_cmds = ["<WK=WR,0>"] + ["<WK=WR,{}>".format(i) for i in range(2, 10)]
        for i in range(1, 10):
            builder = WalkCommandBuilder(WalkDirection.right, steps=i)
            actual_cmd = builder.build()
            expected_cmd = expected_cmds[i - 1]
            self.assertEqual(expected_cmd, actual_cmd)


class TestMotorCommandBuilder(unittest.TestCase):

    def test_invalid_range(self):
        # Make sure valid ranges don't raise exceptions
        try:
            MotorCommandBuilder(MotorId.head_turn, 0., 0.)
            MotorCommandBuilder(MotorId.head_turn, 1., 10.)
        except ValueError:
            self.fail("MotorCommandBuilder raised ValueError when it shouldn't")

        # Test invalid motor positions
        with self.assertRaises(ValueError):
            MotorCommandBuilder(MotorId.head_turn, -0.1, 0.)

        with self.assertRaises(ValueError):
            MotorCommandBuilder(MotorId.head_turn, 1.1, 0.)

        # Test invalid motor duration
        with self.assertRaises(ValueError):
            MotorCommandBuilder(MotorId.head_turn, 0., -0.1)

        with self.assertRaises(ValueError):
            MotorCommandBuilder(MotorId.head_turn, 0., 10.1)


if __name__ == '__main__':
    unittest.main()
