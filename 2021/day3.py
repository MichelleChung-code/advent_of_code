import collections
import unittest
from typing import List

import pandas as pd


def binary_diagnostic(binary_input: List[str]) -> float:
    """
    Compute the "gamma" and "epsilon" rates from the binary report.  Where:
    gamma: most common bit per position (all appended together for the final "rate")
    epsilon: least common bit per position (all appended together for the final "rate")

    Then the final return will be the power consumption, which is the "gamma" and "epsilon" rates in their decimal forms
    multiplied.

    Args:
        binary_input: <list> of strings of the binary diagnostic report

    Returns:
        power consumption: <float> multiplication of the decimal representations of the gamma and epsilon rate
    """
    # generate the gamma and epsilon rate

    # gamma rate is the binary number resulting from the most common bit per position
    # epsilon rate is the binary number resulting from the least common bit per position

    # split into characters by typecasting into list
    binary_ls = list(map(list, binary_input))

    df = pd.DataFrame(binary_ls)

    # get the most and least common element per column
    # by definition, can only be either 0 or 1

    most_common_ls = []
    least_common_ls = []
    for col in df.columns:
        dict_count = collections.Counter(df[col])
        # order in ascending order by the values
        dict_count = dict(sorted(dict_count.items(), key=lambda item: item[1]))

        # if there are Nones - however, should not happen
        # if None in dict_count.keys():
        #     dict_count.pop(None)

        most_common_ls.append(list(dict_count.keys())[-1])
        least_common_ls.append(list(dict_count.keys())[0])

    gamma = ''.join(most_common_ls)
    epsilon = ''.join(least_common_ls)

    # power rate is the decimal representation of gamma * epsilon
    return int(gamma, 2) * int(epsilon, 2)


def binary_diagnostic_part2(binary_input: list) -> float:
    # todo
    return


class TestBinaryDiagnostic(unittest.TestCase):
    def test_binary_diagnostic(self):
        ls_test_input = ['00100',
                         '11110',
                         '10110',
                         '10111',
                         '10101',
                         '01111',
                         '00111',
                         '11100',
                         '10000',
                         '11001',
                         '00010',
                         '01010']

        self.assertEqual(198, binary_diagnostic(ls_test_input))


if __name__ == '__main__':
    # we need to read this in with the string converter, otherwise it
    df = pd.read_csv(r'./mfs_inputs/day3.csv', converters={'value': str})
    problem_bin_input = list(df['value'])
    # problem_bin_input = list(map(str, problem_bin_input)) # using the converters when read in, instead

    print(binary_diagnostic(problem_bin_input))
