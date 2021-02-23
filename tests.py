import unittest
from entities import *
from service import *


class test_entities(unittest.TestCase):
    def test_set_board(self):
        board = Board()
        board.set_board([1])
        assert len(board._data) == 1 and board._data[0] == 1

    def test_get_board(self):
        board = Board()
        board.set_board([1])
        b = board.get_board()
        assert b == [1]

    def test_set(self):
        board = Board()
        board.set_board([1])
        board.set(0, 5)
        b = board.get_board()
        assert len(b) == 1 and b[0] == 5

    def test_get(self):
        board = Board()
        board.set_board([1, 2, 3])
        value = board.get(1)
        assert value == 2


board = Board()
service = Service(board)


class test_service(unittest.TestCase):
    def test_get_board(self):
        b = service.get_board()
        assert isinstance(b, Board) and len(b._data) == 42

    def test_place(self):
        service.place(0, 111)
        b = service.get_board()
        assert b.get(0) == 111

    def test_is_full(self):
        # non-full board
        for i in range(6):
            service.place(i, 1)
        assert service.is_full() == False
        # full board
        service.place(6, 1)
        assert service.is_full() == True

    def test_get_value(self):
        service.place(0, 111)
        b = service.get_board()
        assert b.get(0) == service.get_value(0)

    def test_validate_column(self):
        column = 'abc'
        try:
            validate_column(column)
            assert False
        except InvalidColumn:
            assert True

        column = 78
        try:
            validate_column(column)
            assert False
        except InvalidColumn:
            assert True

    def test_first_available_position(self):
        service.place(41, 1)
        service.place(34, 1)
        assert service.first_available_position(6) == 27
        for p in range(35, -1, -7):
            service.place(p, 1)
        assert service.first_available_position(0) == -1

    def test_player_move(self):
        for p in range(42):
            service.place(p, 1)
        try:
            service.player_move(1, 1)
            assert False
        except Tie:
            assert True

        for p in range(42):
            service.place(p, 0)

    def test_computer_move(self):
        # computer makes winning move
        service.place(38, 1)
        service.place(31, 1)
        service.place(24, 1)
        try:
            service.computer_move(1)
            assert False
        except ComputerWon as error:
            assert str(error) == 'computer won!'
        # computer blocks player from winning
        service.place(38, -1)
        service.place(31, -1)
        service.place(24, -1)
        service.computer_move(1)
        assert service.get_value(17) == 1

    def test_win_on_line(self):
        for i in range(42):
            service.place(i, 0)
        for i in range(28, 32):
            service.place(i, 1)
        assert service.win_on_line(29) == True
        service.place(30, 0)
        assert service.win_on_line(29) == False

    def test_win_on_column(self):
        for i in range(42):
            service.place(i, 0)
        for i in range(18, 39, 7):
            service.place(i, 1)
        assert service.win_on_column(25) == False
        service.place(39, 1)
        assert service.win_on_column(25) == True

    def test_win_on_diagonal_one(self):
        for i in range(42):
            service.place(i, 0)
        for i in range(9, 33, 8):
            service.place(i, 1)
        assert service.win_on_diagonal_one(17) == False
        service.place(33, 1)
        assert service.win_on_diagonal_one(17) == True

    def test_win_on_diagonal_two(self):
        for i in range(11, 29, 6):
            service.place(i, 1)
        assert service.win_on_diagonal_two(17) == False
        service.place(29, 1)
        assert service.win_on_diagonal_two(17) == True
