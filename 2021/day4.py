from typing import List

import numpy as np
import pandas as pd


def bingo_score(binary_input: List[str]) -> float:
    return None


def read_text_file(file_name):
    with open(file_name, 'r') as f:
        arr = f.read().splitlines()

    draw_order_ls = list(map(int, arr[0].split(',')))
    arr = arr[2:]

    bingo_sheets_ls = []
    indiv_arr = []
    for line in arr:
        if not line:
            bingo_sheets_ls.append(pd.DataFrame(np.asarray(indiv_arr)))
            indiv_arr = []
            continue

        # replace any double spaces with single spaces
        line = line.replace('  ', ' ').strip()
        indiv_arr.append(list(map(int, line.split(' '))))

    return draw_order_ls, bingo_sheets_ls


if __name__ == '__main__':
    draw_order_ls, bingo_sheets_ls = read_text_file(r'./mfs_inputs/day4_part1_sample.txt')
