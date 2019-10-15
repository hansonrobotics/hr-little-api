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

from hr_little_api.json_api import json_length, generate_id


class TestJsonApi(unittest.TestCase):

    def test_json_length(self):
        self.assertEqual('000000', json_length(""))
        self.assertEqual('000001', json_length("a"))
        self.assertEqual('000010', json_length("a" * 10))
        self.assertEqual('004090', json_length("a" * 4090))

        with self.assertRaises(ValueError):
            json_length("a" * 4091)

    def test_generate_id(self):
        callback_id = generate_id()
        self.assertTrue(callback_id.startswith("cb."))
        self.assertLessEqual(len(callback_id), 25)


if __name__ == '__main__':
    unittest.main()
