import numpy as np
import pandas as pd


def bingo_score(draw_order_ls, bingo_sheets_ls) -> float:
    for elem in draw_order_ls:
        for i in range(len(bingo_sheets_ls)):
            bingo_sheets_ls[i] = bingo_sheets_ls[i].replace(elem, np.NaN)
            # check if there is either a row or a column that is all NaN
            win_row_bool = bingo_sheets_ls[i].isnull().apply(lambda x: all(x), axis=1).any()
            win_col_bool = bingo_sheets_ls[i].isnull().apply(lambda x: all(x), axis=0).any()

            if win_row_bool or win_col_bool:
                # there is a winner
                return bingo_sheets_ls[i].sum().sum() * elem


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

    # append the last dataframe
    bingo_sheets_ls.append(pd.DataFrame(np.asarray(indiv_arr)))

    return draw_order_ls, bingo_sheets_ls


if __name__ == '__main__':
    draw_order_ls, bingo_sheets_ls = read_text_file(r'./mfs_inputs/day4_part1_sample.txt')
    assert bingo_score(draw_order_ls, bingo_sheets_ls) == 4512

    # actual problem
    draw_order_ls, bingo_sheets_ls = read_text_file(r'./mfs_inputs/day4.txt')
    print(bingo_score(draw_order_ls, bingo_sheets_ls))


