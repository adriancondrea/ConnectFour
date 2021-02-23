import random
from exceptions import *


def validate_column(column):
    """
    validates the column variable, read from the keyboard.
    Raises a value error if it is not an integer between 0 and 6
    """
    try:
        column = int(column)
    except ValueError:
        raise InvalidColumn('column must be a number between 0 and 6!')

    if column < 0 or column > 6:
        raise InvalidColumn('invalid column!')
    return column


class Service:
    def __init__(self, board):
        self._board = board

    def get_board(self):
        """
        :return: the game board
        """
        return self._board

    def is_full(self):
        """
        Checks if the board is full. If we find a 0 on the last line of the board, it is not full
        :return: True if the board is full, False otherwise
        """
        for i in range(0, 7):
            if self.get_value(i) == 0:
                return False
        return True

    def place(self, position, value):
        """
        puts 'value' at index 'position' in the board
        :param position: position of the value we want to change
        :param value: the value we want to place
        """
        self._board.set(position, value)

    def get_value(self, position):
        """
        :return: returns the value at index 'position' from the board
        """
        return self._board.get(position)

    def first_available_position(self, column):
        """
        :param column: a column between 0 and 6
        :return: returns the index of the first available position on the given column (the greatest index
        of the element from the board which is on the given column and whose value is equal to 0)
        returns -1 if the column is full
        """
        position = (42 + column) - 7
        # the element situated on given column, first line (bottom of the board)
        while position >= 0:
            if self._board.get(position) == 0:
                return position
            # we subtract 7, because we want to stay on the same column
            position -= 7
        return -1

    def player_move(self, column, value):
        """
        puts 'value' on 'column' in the first empty position (highest index). It raises Tie exception
        if the game is a tie, FullColumn if the column we try to place on is full and PlayerWon if
        the player won the game
        :return:
        """
        if self.is_full():
            raise Tie('tie!')
        position = self.first_available_position(column)
        if position == -1:
            raise FullColumn('column is full!')
        self.place(position, value)
        if self.check_won(position):
            raise PlayerWon('player won!')

    def make_random_move(self, value):
        """
        places 'value' on a random column on the board, at the highest empty index
        :param value:
        :return:
        """
        columns = list(range(0, 7))
        # while we haven't tried placing the piece on all columns
        while len(columns) > 0:
            # we take a random column to try place the piece on, then remove it from the list
            column = random.choice(columns)
            columns.remove(column)
            position = self.first_available_position(column)
            # if we can place the piece on that column, we do that and exit the function
            if position != -1:
                self.place(position, value)
                return

    def computer_move(self, value):
        """
        makes the computer's choice. If the computer can win, he will perform the winning move. Otherwise, if he can
        stop the player from a one-move victory he does that. If he can't do either one of those two, he will perform a
        random move
        Raises Tie if the board is full (tie)
        Raises ComputerWon if the computer won
        :param value:
        :return:
        """
        if self.is_full():
            raise Tie('tie!')
        # we make a board copy, because we will alter the board while looking for a winning move
        board_copy = self._board.get_board()
        for column in range(7):
            self._board.set_board(board_copy)
            position = self.first_available_position(column)
            if position != -1:
                self.place(position, value)
                # we check for a won game. If it is won, we raise an exception and stop the execution of this function.
                # otherwise, we will try the next column, if there are any left
                if self.check_won(position):
                    raise ComputerWon('computer won!')

        # if we got there it means we couldn't find a winning move. Now we are looking to block a winning move from the
        # player which can occur on his turn
        for column in range(7):
            self._board.set_board(board_copy)
            position = self.first_available_position(column)
            if position != -1:
                # we emulate the player's turn and check for a winning move. If we find it, we block it and stop this
                # function
                self.place(position, value * -1)
                if self.check_won(position):
                    self.place(position, value)
                    return
        # if we get there, it means we couldn't make a winning move and we didn't find a winning move the player can
        # make in the next turn. So we perform a random move.
        self._board.set_board(board_copy)
        self.make_random_move(value)

    def win_on_line(self, position):
        """
        checks from a win on line, by having 4 or more equal consecutive elements on that line, starting from position
        :return: returns True if the game is won on line, False otherwise
        """
        line = 1  # number of consecutive equal elements on line
        index = 1
        # we look to the right of our element until the end of the line or until we find the first distinct elements
        # and count the number of consecutive elements that are equal
        while (position + index) % 7 != 0 and position + index <= 41 and self.get_value(position) == self.get_value(
                position + index):
            line += 1
            index += 1

        # we look to the left of our element now
        index = 1
        while position - index >= 0 and (position - index) % 7 != 6 and self.get_value(position) == self.get_value(
                position - index):
            line += 1
            index += 1
        if line >= 4:
            return True
        return False

    def win_on_column(self, position):
        """
        checks for a win on columns, that includes the element on given position
        :param position:
        :return: True if we find a winning combination, False otherwise
        """
        column = 1  # number of consecutive equal elements on column
        index = 7
        # check below our element
        while position + index <= 41 and self.get_value(position) == self.get_value(position + index):
            column += 1
            index += 7

        # check above our element
        index = 7
        while position - index >= 0 and self.get_value(position) == self.get_value(position - index):
            column += 1
            index += 7
        if column >= 4:
            return True
        return False

    def win_on_diagonal_one(self, position):
        """
        we check for a win on the first diagonal
        :param position:
        :return: True if the game is won, False otherwise
        """
        diagonal1 = 1  # number of consecutive equal elements on diagonal
        index = 8
        while position + index <= 41 and self.get_value(position) == self.get_value(position + index):
            diagonal1 += 1
            current_position = position + index
            if (35 <= current_position <= 41) or current_position % 7 == 6:
                break
            index += 8

        index = 8
        while position - index >= 0 and self.get_value(position) == self.get_value(position - index):
            diagonal1 += 1
            current_position = position - index
            if (0 <= current_position <= 6) or current_position % 7 == 0:
                break
            index += 8
        if diagonal1 >= 4:
            return True
        return False

    def win_on_diagonal_two(self, position):
        """
        Checks for a win on the second diagonal
        :param position:
        :return: True if the game is won, False otherwise
        """
        diagonal2 = 1  # number of consecutive equal elements on diagonal
        index = 6
        while position + index <= 41 and self.get_value(position) == self.get_value(position + index):
            diagonal2 += 1
            current_position = position + index
            if (35 <= current_position <= 41) or current_position % 7 == 0:
                break
            index += 6

        index = 6
        while position - index >= 0 and self.get_value(position) == self.get_value(position - index):
            diagonal2 += 1
            current_position = position - index
            if (0 <= current_position <= 6) or current_position % 7 == 6:
                break
            index += 6
        if diagonal2 >= 4:
            return True
        return False

    def check_won(self, position):
        return self.win_on_line(position) or self.win_on_column(position) or self.win_on_diagonal_one(
            position) or self.win_on_diagonal_two(position)
