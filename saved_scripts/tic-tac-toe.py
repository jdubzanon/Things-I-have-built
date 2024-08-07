import numpy as np
board = np.array([['11','12','13'],['21','22','23'],['31','32','33']])


def conversion(selection):
    convert = {
        '1': '0',
        '2': '1',
        '3': '2'
    }
    lst1 = [num for num in str(selection)]

    first_number = int(convert.get(lst1[0], None))
    second_number = int(convert.get(lst1[1], None))
    return [int(first_number),int(second_number)]


def error_check(board, coordinates, turn):
    if turn == 0:
        if not board[coordinates[0]][coordinates[1]].isnumeric():
            print('Player One Please Choose Another Number!!!')
            turn -= 1
        else:
            turn = 0
    if turn == 1:
        if not board[coordinates[0]][coordinates[1]].isnumeric():
            print('Player Two Please Choose Another Number!!!')
            turn += 1
        else:
            turn = 1
    return turn

def board_placement(coordinates,board,turn):
    if turn == 0:
        if board[coordinates[0]][coordinates[1]].isnumeric():
            board[coordinates[0]][coordinates[1]] = 'X'

    if turn == 1:
        if board[coordinates[0]][coordinates[1]].isnumeric():
            board[coordinates[0]][coordinates[1]] = 'O'
    return board

def directions():
    example = np.array([['X', '12', '13'], ['21', '22', '23'], ['31', '32', '33']])
    print('''DIRECTIONS!!!!!!!!: 
        Whatever spot you want to put your character in type in that number. For example if you want to 
        put an X in the top left corner choose the number 11''')
    print(example)


game_over = False
turn = 0
directions()
while game_over is False:

    if turn == 0:
        selection = (input('Player1 choose location '))
    else:
        selection = input('Player2 choose location ')
    if selection == 'quit':
        break
    if turn == 0:
        try:
            coordinates = conversion(selection)
            turn = error_check(board,coordinates,turn)
        except TypeError:
            print('Player Please Choose Another Number')
            turn -= 1
        except UnboundLocalError:
            print('Player Please Choose Another Number')
            turn -= 1

    if turn == 1:
        try:
            coordinates = conversion(selection)
            turn = error_check(board,coordinates,turn)
        except TypeError:
            print('Player Please Choose Another Number')
            turn += 1
        except UnboundLocalError:
            print('Player Please Choose Another Number')
            turn += 1

    print(board_placement(coordinates, board, turn))

    turn += 1
    turn = turn % 2
