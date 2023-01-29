import unittest
from pathlib import Path

from physicool import processing

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data"


def make_df_from_positions(path: Path) -> pd.DataFrame:
    """Returns a Dataframe with the output structure based on the initial cell values (csv)."""
    data = pd.read_csv(
        path, names=["position_x", "position_y", "position_z", "definition"]
    )
    data = data.drop(columns=["definition"])
    data["ID"] = [float(i) for i in data.index]
    data["timestep"] = 0
    data = data.reindex(
        columns=["ID", "position_x", "position_y", "position_z", "timestep"]
    )

    return data


class TestReadCellData(unittest.TestCase):
    def test_read_positions(self):
        """Asserts that the cell positions are read correctly."""
        expected_data = make_df_from_positions(DATA_PATH / "cells.csv")
        data = processing.get_cell_data(
            timestep=0,
            variables=["ID", "position_x", "position_y", "position_z"],
            output_path=DATA_PATH,
            version="1.9.1",
        )

        pd.testing.assert_frame_equal(data, expected_data)


class TestOutputProcessor(unittest.TestCase):
    def test_get_number_of_cells(self):
        """Asserts that the processing function reads the number of cells over time correctly."""
        number_of_cells = processing.get_cell_numbers_over_time(
            output_path=DATA_PATH, version="1.9.1"
        )
        np.testing.assert_array_equal(np.asarray([19, 19]), number_of_cells)


if __name__ == "__main__":
    unittest.main()
