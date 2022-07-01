import unittest

from physicool import processing

import pandas as pd

EXPECTED_POSITIONS = pd.read_csv("data/initial_positions.csv")
DATA_PATH = "data"


class TestReadCellData(unittest.TestCase):
    def test_read_positions(self):
        """Asserts that the cell positions are read correctly."""
        data = processing.get_cell_data(timestep=0,
                                        variables=["ID", "position_x", "position_y", "position_z"],
                                        output_path=DATA_PATH)

        pd.testing.assert_frame_equal(data, EXPECTED_POSITIONS)


class TestOutputProcessor(unittest.TestCase):
    def test_get_number_of_cells(self):
        """Asserts that the processing function reads the number of cells over time correctly."""
        number_of_cells = processing.get_cell_numbers_over_time(output_path=DATA_PATH)
        self.assertEqual([3], number_of_cells)


if __name__ == '__main__':
    unittest.main()
