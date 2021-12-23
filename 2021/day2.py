import copy
import unittest

import pandas as pd

position_map_horizontal = {'forward': 1}
position_map_vertical = {'down': 1,
                         'up': -1}
merged_position_map = copy.deepcopy(position_map_vertical)
merged_position_map.update(position_map_horizontal)


def dive(movements: pd.DataFrame) -> float:
    """
    Compute the final positions of where the submarine lands, given input movement instructions

    Args:
        movements: dataframe containing directions and quantity of units to move in each direction

    Returns:
        multiplication of the final horizontal position and depth
    """
    movements[['direction', 'amount']] = movements['value'].str.split(' ', 1, expand=True)
    movements['amount'] = movements['amount'].astype(int)
    movements['implied_dir'] = movements['direction'].map(merged_position_map)
    movements['pos_update'] = movements['amount'] * movements['implied_dir']

    x = movements.loc[movements['direction'].isin(position_map_horizontal.keys())]['pos_update'].sum()
    y = movements.loc[movements['direction'].isin(position_map_vertical.keys())]['pos_update'].sum()

    return x * y


class TestDive(unittest.TestCase):
    def test_dive_position(self):
        test_input = pd.DataFrame(['forward 5',
                                   'down 5',
                                   'forward 8',
                                   'up 3',
                                   'down 8',
                                   'forward 2'], columns=['value'])
        self.assertEqual(150, dive(test_input))


if __name__ == '__main__':
    df = pd.read_csv(r'./mfs_inputs/day2.csv')
    # depths = list(df.values.flatten())

    print(dive(df))
