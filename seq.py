#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Simon Rüegg
# sequential.py

import time

BOARD_SIZE = 14
solutions = []
solution_count = 0


def under_attack(col, row):
    if row in solutions:
        return True
    for act_col, act_row in enumerate(solutions):
        if act_col + act_row == col + row:
            return True
        elif act_row - act_col == row - col:
            return True
    return False


def place_queen(col):
    global solutions, solution_count
    if len(solutions) == BOARD_SIZE:
        solution_count += 1
    else:
        for row in range(BOARD_SIZE):
            if not under_attack(col, row):
                solutions.append(row)
                place_queen(col + 1)
                solutions.pop()

start = time.time()
place_queen(0)
end = time.time()

print "Board size: {}".format(BOARD_SIZE)
print "Solution count: {}".format(solution_count)
print "Runtime in s: {}".format(end - start)
