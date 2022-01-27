import unittest

from physicool import config


class MyTestCase(unittest.TestCase):
    def get_cell_definition_list(self):
        xml_data = config.ConfigFileParser()
        cell_list = xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default"])


if __name__ == '__main__':
    unittest.main()
