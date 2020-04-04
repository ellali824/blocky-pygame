"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement Me
    # COLOUR_LIST has 4 colors. so num_goals <= 4
    x = random.randint(0, 1)
    goal_lst = []
    num_lst = [0, 1, 2, 3]

    for i in range(num_goals):
        index = random.choice(num_lst)

        if x == 0:  # Perimeter Goal
            goal_lst.append(PerimeterGoal(COLOUR_LIST[index]))
        else:
            goal_lst.append(BlobGoal(COLOUR_LIST[index]))

        num_lst.remove(index)

    return goal_lst


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement me
    lst_blocks = _create_list_blocks(block)
    big_lst = []
    x = 0
    for i in range(pow(2, block.max_depth - block.level)):
        small_lst = []
        y = 0

        _fill_inner_lst(block, lst_blocks, small_lst, x, y)

        big_lst.append(small_lst)

        x += block.size / pow(2, block.max_depth - block.level)

    tuple_lst = []
    for i in range(len(big_lst)):
        col_lst = []

        for j in range(len(big_lst[i])):
            col_lst.append(big_lst[i][j].colour)

        tuple_lst.append(col_lst)

    return tuple_lst


# helper functions
def _fill_inner_lst(block: Block, lst_blocks: List[Block],
                    small_lst: List[Block], x: int, y: int) -> None:
    """Add the appropriate blocks from <lst_blocks> to <small_lst>.

    :param block:
    :param lst_blocks:
    :param small_lst:
    :return:
    """
    while len(small_lst) < pow(2, block.max_depth - block.level):
        for b in lst_blocks:
            if _location_in_block(b, (x, y)):
                small_lst.append(b)
                return None

        y += block.size / pow(2, block.max_depth - block.level)


def _create_list_blocks(block: Block) -> List[Block]:
    """Return a list of all the Blocks that need to be drawn in order to create
    <block>. (all the leaves of the tree)
    :param block:
    :return:
    """
    if block.children == []:
        return [block]
    else:
        lst = []
        for child in block.children:
            lst.extend(_create_list_blocks(child))

        return lst


def _location_in_block(block: Block, location: Tuple[int, int]) -> bool:
    """Return True if <location> is in <block>. Return False otherwise.
    :param block:
    :param location:
    :return:
    """
    block_x = block.position[0]
    block_y = block.position[1]
    loc_x = location[0]
    loc_y = location[1]
    if block_x <= loc_x < block_x + block.size and \
            block_y <= loc_y < block_y + block.size:
        return True
    return False


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):

    def score(self, board: Block) -> int:
        # TODO: Implement me
        lst_lst_tup = _flatten(board)
        score = 0
        for i in range(len(lst_lst_tup)):
            for j in range(len(lst_lst_tup[i])):
                if lst_lst_tup[i][j] == self.colour:
                    score += 1
        # corners
        max_index = pow(2, board.max_depth) - 1
        if lst_lst_tup[0][0] == self.colour:
            score += 1
        if lst_lst_tup[0][max_index]:
            score += 1
        if lst_lst_tup[max_index][0]:
            score += 1
        if lst_lst_tup[max_index][max_index]:
            score += 1

        return score

    def description(self) -> str:
        # TODO: Implement me
        return 'Most unit cells of ' + colour_name(self.colour) + \
               ' on the perimeter'


class BlobGoal(Goal):
    def score(self, board: Block) -> int:
        # TODO: Implement me
        brd = _flatten(board)
        v = []
        for i in range(len(brd)):
            lst = []
            for j in range(len(brd)):
                lst.append(-1)
            v.append(lst)
        scores = []
        for i in range(len(brd)):
            for j in range(len(brd)):
                scores.append(self._undiscovered_blob_size((i, j), brd, v))
        return max(scores)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # TODO: Implement me
        sc = 1
        i = pos[0]
        j = pos[1]
        if board[i][j] != self.colour:
            visited[i][j] = 0
            return 0
        if 0 > i >= len(board) or 0 > j >= len(board):
            return 0
        visited[i][j] = 1
        for n in range(4):
            if n == 0 and i + 1 < len(board) and visited[i + 1][j] == -1:
                sc += self._undiscovered_blob_size((i + 1, j), board, visited)
            if n == 1 and i + 1 < len(board) and visited[i][j + 1] == -1:
                sc += self._undiscovered_blob_size((i, j + 1), board, visited)
            if n == 2 and i - 1 >= 0 and visited[i - 1][j] == -1:
                sc += self._undiscovered_blob_size((i - 1, j), board, visited)
            if n == 3 and j - 1 >= 0 and visited[i][j - 1] == -1:
                sc += self._undiscovered_blob_size((i, j - 1), board, visited)
        return sc

    def description(self) -> str:
        # TODO: Implement me
        return 'Largest group of connected blocks of ' + \
               colour_name(self.colour)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
