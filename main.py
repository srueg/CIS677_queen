#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Simon Rüegg
# parallel.py

import numpy
import math
from mpi4py import MPI
import sys
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
workers = size - 1
name = MPI.Get_processor_name()
MASTER = 0

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

if rank == MASTER:
    solutions = 0
    start = time.time()
    chunk = int(max(1, math.ceil(float(BOARD_SIZE) / workers)))
    for i in range(1, size):
        comm.send(chunk, dest=i, tag=1)

    for i in range(1, size):
        s = comm.recv(tag=2)
        # print "Received {} solutions from {}".format(s, i)
        solutions += s

    end = time.time()
    print "Board size: {}".format(BOARD_SIZE)
    print "Solution count: {}".format(solutions)
    print "Runtime in s: {}".format(end - start)
else:
    c = comm.recv(source=MASTER, tag=1)
    #sys.stdout.write("Start row %d for P%d on %s.\n" % (start_row, rank, name))
    start = (rank - 1) * c
    for i in range(start, start + c):
        #sys.stdout.write("Starting with row %d on P%d\n" % (i, rank))
        if i < BOARD_SIZE:
            solutions = []
            solutions.append(i)
            place_queen(1)
    #sys.stdout.write("Solutions: %d\n" % (solution_count))
    comm.send(solution_count, dest=MASTER, tag=2)
