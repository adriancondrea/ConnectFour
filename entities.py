from texttable import Texttable
from copy import deepcopy


class Board:
    def __init__(self):
        self._data = [0] * 42  # the game board

    def __str__(self):
        """
        :return: the game board as a string, formatted using Texttable module
        """
        t = Texttable()
        # dictionary translating the values from the board to their string equivalent (the way we want to print them)
        d = {-1: 'Y', 0: '-', 1: 'R'}

        for i in range(0, 41, 7):
            # we take each row of the board
            row = self._data[i:i + 7]
            # translate the row to its string equivalent
            for j in range(7):
                row[j] = d[row[j]]
            # add the row to the texttable t
            t.add_row(row)
        return t.draw()

    def set_board(self, board):
        """
        sets the _data field of the board equal to a copy of the board variable
        :param board: the board we want to save in _data
        :return:
        """
        self._data = deepcopy(board)

    def get_board(self):
        """
        :return: a copy of the board as a list
        """
        return self._data[:]

    def set(self, position, value):
        """
        sets the element at position equal to value
        """
        self._data[position] = value

    def get(self, position):
        """
        :param position: the index of the value we want to return
        :return: the value at index position in _data list
        """
        return self._data[position]
