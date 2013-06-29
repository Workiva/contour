import unittest
import os

from mock import patch

from contour import Contour


class ContourTestCase(unittest.TestCase):

    def test_load_config_from_file(self):
        """Ensure Contour will load a specified path."""
        path = os.path.join('contour', '_contour.yaml')
        c = Contour(path)

        self.assertEqual(c["session"], "test")
        self.assertEqual(c, {"session": "test"})

    def test_load_local_config_from_file(self):
        """Ensure Contour will load a specified path from local."""
        path = os.path.join('contour', '_contour_local.yaml')

        c = Contour(path)

        self.assertEqual(c["session"], "localtest")
        self.assertEqual(c, {"session": "localtest"})

    def test_load_config_from_name_with_no_extension(self):
        """Ensure Contour will load a specified name."""
        c = Contour("_contour")

        self.assertEqual(c, {"session": "test"})

    def test_load_config_from_name_with_extension(self):
        """Ensure Contour will load a specified name with an extension."""
        c = Contour("_contour.yaml")

        self.assertEqual(c, {"session": "test"})

    def test_config_from_defaults(self):
        """Ensure Contour will set the defaults passed into the init."""
        defaults = {
            'test': 'foo'
        }
        c = Contour(defaults=defaults)

        self.assertEqual(c, defaults)

    def test_file_overrides_defaults(self):
        """Ensure Contour will set the defaults and override them with the
        file.
        """
        defaults = {
            'session': 'foo'
        }
        c = Contour("_contour.yaml", defaults=defaults)

        self.assertEqual(c, {"session": "test"})

    def test_local_overrides_defaults(self):
        """Ensure Contour will set the defaults and override them with the
        local file.
        """
        defaults = {
            'session': 'foo'
        }
        c = Contour("_contour_local.yaml", defaults=defaults)

        self.assertEqual(c, {"session": "localtest"})

    def test_local_overrides_standard(self):
        """Ensure Contour will load the standard config file and override it
        with the local file.
        """
        c = Contour(config_name="_contour.yaml",
                    local_config_name="_contour_local.yaml")

        self.assertEqual(c, {"session": "localtest"})


class TestConfigurationLoading(unittest.TestCase):

    def test_load_yaml_config(self):
        """Ensure _load_yaml_config will load a specified path."""
        from contour.contour import _load_yaml_config

        contents = _load_yaml_config(os.path.join('contour', '_contour.yaml'))

        self.assertEqual(contents, "session: test\n")

    def test_module_import_missing_module(self):
        """Ensure module_import raises an exception when the specified module
        does not exist.
        """
        from contour import BadModulePathError
        from contour import module_import

        self.assertRaises(BadModulePathError,
                          module_import, 'contour.extras.not_here')

    def test_module_import(self):
        """Ensure module_import returns a reference to the expected module."""
        from contour import module_import
        from contour import contour

        module = module_import('contour.contour')

        self.assertEqual(module, contour)

    @patch('os.path.exists', autospec=True)
    def test_not_find_yaml(self, mock_exists):
        """Ensure when no contour.yaml exists, no file is found."""
        mock_exists.return_value = False

        from contour import find_contour_yaml

        config_yaml_path = find_contour_yaml()

        self.assertIsNone(config_yaml_path)

    def test_get_config(self):
        """Ensure a contour contents produces the expected dictionary."""
        from contour.contour import _parse_yaml_config

        example_yaml = str('secret_key: "blah"\n'
                           'persistence: bubble\n'
                           'task_system: flah\n')

        my_config = _parse_yaml_config(example_yaml)

        self.assertEqual(my_config, {'secret_key': 'blah',
                                     'persistence': 'bubble',
                                     'task_system': 'flah'})

    def test_get_config_invalid_yaml(self):
        """Ensure an invalid yaml file will raise InvalidYamlFile."""
        from contour import InvalidYamlFile
        from contour.contour import _parse_yaml_config

        example_yaml = str('secret_key:"blah"\n'
                           'persistence:bubble\n'
                           'task_system:flah\n')

        self.assertRaises(InvalidYamlFile, _parse_yaml_config, example_yaml)

    def test_get_config_empty_yaml(self):
        """Ensure an empty contour.yaml will produce a default config."""
        from contour.contour import _parse_yaml_config

        example_yaml = str('')

        my_config = _parse_yaml_config(example_yaml)

        self.assertEqual(my_config, {})
