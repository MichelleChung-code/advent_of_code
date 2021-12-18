import unittest
from typing import List

import pandas as pd


def sonar_sweep(depths: List) -> int:
    """
    Day 1 Part 1
    Get the number of times the current sweep was deeper than the previous
    Args:
        depths: list of depths

    Returns:
        number of sweeps where current was larger than previous
    """
    counter = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i - 1]:
            counter += 1

    return counter


def sonar_sweep_sliding_window(depths: pd.DataFrame, window: int = 3) -> int:
    """
    Day 1 Part 2
    Get the number of times the current sweep was deeper than the previous.  But now this is based on a rolling sum.
    Args:
        depths: dataframe where the raw depths are the values
        window: window to compute the rolling sum on

    Returns:
        number of sweeps where current was larger than previous based on a rolling sum
    """
    # get the rolling sums and drop the NaN (beginning of the window)
    rolling_depths = depths.rolling(window=window).sum().dropna()
    return sonar_sweep(rolling_depths.values.flatten())


class TestSonarSweep(unittest.TestCase):
    def test_sonar_sweep(self):
        test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        self.assertEqual(7, sonar_sweep(test_input))

    def test_sonar_sliding(self):
        test_input = pd.DataFrame([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
        self.assertEqual(5, sonar_sweep_sliding_window(test_input))


if __name__ == '__main__':
    df = pd.read_csv(r'./mfs_inputs/day1.csv')
    # depths = list(df.values.flatten())

    print(sonar_sweep_sliding_window(df))
