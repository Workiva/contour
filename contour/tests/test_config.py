#
# Copyright 2013 WebFilings, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import unittest
import os

from mock import patch


class TestConfigurationLoading(unittest.TestCase):

    def test_load_yaml_config(self):
        """Ensure _load_yaml_config will load a specified path."""
        from contour.config import _load_yaml_config

        contents = _load_yaml_config(os.path.join('contour', '_contour.yaml'))

        self.assertEqual(contents, "session: test\n")

    def test_module_import_missing_module(self):
        """Ensure module_import raises an exception when the specified module
        does not exist.
        """
        from contour.config import BadModulePathError
        from contour.config import module_import

        self.assertRaises(BadModulePathError,
                          module_import, 'contour.extras.not_here')

    def test_module_import(self):
        """Ensure module_import returns a reference to the expected module."""
        from contour.config import module_import
        from contour import config

        module = module_import('contour.config')

        self.assertEqual(module, config)

    @patch('os.path.exists', autospec=True)
    def test_not_find_yaml(self, mock_exists):
        """Ensure when no contour.yaml exists, no file is found."""
        mock_exists.return_value = False

        from contour.config import find_contour_yaml

        config_yaml_path = find_contour_yaml()

        self.assertIsNone(config_yaml_path)

    def test_get_config(self):
        """Ensure a config contents produces the expected dictionary."""
        from contour.config import _parse_yaml_config

        example_yaml = str('secret_key: "blah"\n'
                           'persistence: bubble\n'
                           'task_system: flah\n')

        my_config = _parse_yaml_config(example_yaml)

        self.assertEqual(my_config, {'secret_key': 'blah',
                                     'persistence': 'bubble',
                                     'task_system': 'flah'})

    def test_get_config_invalid_yaml(self):
        """Ensure an invalid yaml file will raise InvalidYamlFile."""
        from contour.config import InvalidYamlFile
        from contour.config import _parse_yaml_config

        example_yaml = str('secret_key:"blah"\n'
                           'persistence:bubble\n'
                           'task_system:flah\n')

        self.assertRaises(InvalidYamlFile, _parse_yaml_config, example_yaml)

    def test_get_config_empty_yaml(self):
        """Ensure an empty contour.yaml will produce a default config."""
        from contour.config import _parse_yaml_config

        example_yaml = str('')

        my_config = _parse_yaml_config(example_yaml)

        self.assertEqual(my_config, {})
