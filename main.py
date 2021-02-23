from ui import UI
from service import Service
from entities import Board

# initialize the board, service and ui objects
board = Board()
service = Service(board)
ui = UI(service)
# run the program
ui.run()
