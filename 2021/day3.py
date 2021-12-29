import collections
import copy
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
    """
    Compute the life support rating, which is implied by the oxygen and CO2 rates that can be found via the binary
    diagnostic report:

    Oxygen: continuously filtering out report entries based on the most common bit at a given position
    CO2: continuously filtering out report entries based on the least common bit at a given position

    If the most and least common bit at a certain position are the same, then: 1 will be taken for the oxygen rate next
    filter and 0 if we are looking for CO2 rate.

    Args:
        binary_input: <list> of strings of the binary diagnostic report

    Returns:
        life support rating: <float> multiplication of the decimal representations of the oxygen and co2 rates
    """
    # generate the oxygen generator and CO2 scrubber rating
    # both of the above numbers are generated using bit criteria listed in: https://adventofcode.com/2021/day/3

    # bits to use when 1 and 0 occurances at a given position are the same
    equal_consideration_dict = {'oxygen': '1',
                                'CO2': '0'}

    # split into characters by typecasting into list
    binary_ls = list(map(list, binary_input))

    oxygen_df = pd.DataFrame(binary_ls)
    co2_df = copy.deepcopy(oxygen_df)

    # get the most and least common element per column
    # by definition, can only be either 0 or 1

    # todo could refactor the two for loops into 1, but we only care about getting the correct answer right now
    for col in oxygen_df.columns:
        if oxygen_df.shape[0] == 1:
            break
        dict_count = collections.Counter(oxygen_df[col])
        # order in ascending order by the values
        dict_count = dict(sorted(dict_count.items(), key=lambda item: item[1]))
        most_common_elem = list(dict_count.keys())[-1]

        # filter the remaining df
        if len(set(dict_count.values())) == 1:  # 1 and 0 occur equally
            oxygen_df = oxygen_df.loc[oxygen_df[col] == equal_consideration_dict['oxygen']]
        else:
            oxygen_df = oxygen_df.loc[oxygen_df[col] == most_common_elem]

    for col in co2_df.columns:
        if co2_df.shape[0] == 1:
            break
        dict_count = collections.Counter(co2_df[col])
        # order in ascending order by the values
        dict_count = dict(sorted(dict_count.items(), key=lambda item: item[1]))
        least_common_elem = list(dict_count.keys())[0]

        # filter the remaining df
        if len(set(dict_count.values())) == 1:
            co2_df = co2_df.loc[co2_df[col] == equal_consideration_dict['CO2']]
        else:
            co2_df = co2_df.loc[co2_df[col] == least_common_elem]

    # life support rating is the multiplication of the decimal representations of oxygen and CO2 rating
    oxygen_rating = oxygen_df.agg(''.join, axis=1).iloc[0]
    co2_rating = co2_df.agg(''.join, axis=1).iloc[0]
    return int(oxygen_rating, 2) * int(co2_rating, 2)


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

    def test_binary_diagnostic_part2(self):
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

        self.assertEqual(230, binary_diagnostic_part2(ls_test_input))


if __name__ == '__main__':
    # we need to read this in with the string converter, otherwise leading zeroes that are significant as we are working
    # in binary, will be cut off
    df = pd.read_csv(r'./mfs_inputs/day3.csv', converters={'value': str})
    problem_bin_input = list(df['value'])
    # problem_bin_input = list(map(str, problem_bin_input)) # using the converters when read in, instead

    print(binary_diagnostic_part2(problem_bin_input))
