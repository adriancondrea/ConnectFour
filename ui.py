from exceptions import *
from service import validate_column


class UI:
    def __init__(self, service):
        self._service = service

    def print_board(self):
        print(self._service.get_board())
        print('\n')

    def run(self):
        self.print_board()
        while True:
            column = input('Enter the column on which you want to place:\n')
            try:
                column = validate_column(column)
            except InvalidColumn as error:
                print(error)
                continue  # move to the next iteration of the while, reading another column because the input was not
                # valid

            # make the player's move
            try:
                self._service.player_move(column, 1)
            except Tie as message:
                print(message)
                return
            except FullColumn as message:
                print(message)
                continue
            except PlayerWon as message:
                print(message)
                self.print_board()
                return
            self.print_board()

            # make the computer's move
            try:
                self._service.computer_move(-1)
            except Tie as message:
                print(message)
                return

            except ComputerWon as message:
                print(message)
                self.print_board()
                return
            self.print_board()
