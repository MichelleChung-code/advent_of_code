from typing import List

import numpy as np
import pandas as pd


def bingo_score(draw_order_ls: list, bingo_sheets_ls: List[pd.DataFrame]) -> float:
    """
    Compute the score of the first bingo sheet to win (either a full row or full column).
    Score is the sum of remaining elements multiplied by the element that caused the board to win.

    Args:
        draw_order_ls: list of elements to draw from (in order)
        bingo_sheets_ls: list of the bingo sheet dataframes in the game

    Returns:
        first winner score
    """
    for elem in draw_order_ls:
        for i in range(len(bingo_sheets_ls)):
            bingo_sheets_ls[i] = bingo_sheets_ls[i].replace(elem, np.NaN)
            # check if there is either a row or a column that is all NaN
            win_row_bool = bingo_sheets_ls[i].isnull().apply(lambda x: all(x), axis=1).any()
            win_col_bool = bingo_sheets_ls[i].isnull().apply(lambda x: all(x), axis=0).any()

            if win_row_bool or win_col_bool:
                # there is a winner
                return bingo_sheets_ls[i].sum().sum() * elem


def bingo_score_win_last(draw_order_ls: list, bingo_sheets_ls: List[pd.DataFrame]) -> float:
    """
    Compute the bingo score of the last winner

    Args:
        draw_order_ls: list of the elements to draw
        bingo_sheets_ls: dataframe list of the bingo sheets in the game

    Returns:
        Score of the last board to win
    """
    steps_to_win_counter = [False] * len(bingo_sheets_ls)
    elem_to_win = [False] * len(bingo_sheets_ls)
    for i in range(len(bingo_sheets_ls)):
        steps_to_win_i = 0

        for elem in draw_order_ls:
            bingo_sheets_ls[i] = bingo_sheets_ls[i].replace(elem, np.NaN)
            # check if there is either a row or a column that is all NaN
            win_row_bool = bingo_sheets_ls[i].isnull().apply(lambda x: all(x), axis=1).any()
            win_col_bool = bingo_sheets_ls[i].isnull().apply(lambda x: all(x), axis=0).any()
            steps_to_win_i += 1

            if win_row_bool or win_col_bool:
                # there is a winner
                steps_to_win_counter[i] = steps_to_win_i
                elem_to_win[i] = elem
                break
            elif not win_row_bool and not win_col_bool and elem == draw_order_ls[-1]:  # the board just lost completely
                steps_to_win_counter[i] = False
                elem_to_win[i] = False

    index_last_winner = steps_to_win_counter.index(max(steps_to_win_counter))

    return bingo_sheets_ls[index_last_winner].sum().sum() * elem_to_win[index_last_winner]


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
    assert bingo_score_win_last(draw_order_ls, bingo_sheets_ls) == 1924

    # actual problem
    draw_order_ls, bingo_sheets_ls = read_text_file(r'./mfs_inputs/day4.txt')
    print(bingo_score(draw_order_ls, bingo_sheets_ls))
    print(bingo_score_win_last(draw_order_ls, bingo_sheets_ls))
