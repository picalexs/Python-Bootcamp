'''
A simple Tic Tac Toe game
'''
import random

def display_board(board):
    '''
    A simple function used to display the board
    '''
    nr_of_markers=0
    for m in board[1:]:
        nr_of_markers+=1
        print(f'| {m} ',end="")
        if nr_of_markers%3==0:
            print('|')
    print('-'*13)

def player_input():
    '''
    Function to handle player input for choosing markers
    '''
    while True:
        marker=input("Player1 choose marker (X or O): ")
        if marker=="0":
            marker="O"
        marker=marker.upper()
        if marker not in ['X','O']:
            print("You have to enter either 'X' or 'O'")
            continue
        if marker=="X":
            return ('X','O')
        return ('O','X')

def place_marker(board, marker, position):
    '''
    Function to place a marker on the board
    '''
    board[position]=marker

def check_win_row(board,mark):
    '''
    Function to check if a player has won on a row
    '''
    #First row
    if (board[1]==mark and board[2]==mark and board[3]==mark):
        return True
    #Second row
    if (board[4]==mark and board[5]==mark and board[6]==mark):
        return True
    #Third row
    if (board[7]==mark and board[8]==mark and board[9]==mark):
        return True
    return False

def check_win_column(board, mark):
    '''
    Function to check if a player has won on a column
    '''
    #First column
    if (board[1]==mark and board[4]==mark and board[7]==mark):
        return True
    #Second column
    if (board[2]==mark and board[5]==mark and board[8]==mark):
        return True
    #Third column
    if (board[3]==mark and board[6]==mark and board[9]==mark):
        return True
    return False

def check_win_diagonal(board, mark):
    '''
    Function to check if a player has won on a diagonal
    '''
    #First diagonal
    if (board[1]==mark and board[5]==mark and board[9]==mark):
        return True
    #Second diagonal
    if (board[3]==mark and board[5]==mark and board[7]==mark):
        return True
    return False

def win_check(board, mark):
    '''
    Function to check if a player has won
    '''

    if check_win_row(board, mark):
        return True

    if check_win_column(board, mark):
        return True

    if check_win_diagonal(board, mark):
        return True
    return False

def choose_first():
    '''
    Function to randomly choose which player goes first
    '''
    first_player=random.randint(0,1)
    if first_player==0:
        return 'X'
    return 'O'

def space_check(board, position):
    '''
    Function to check if a position on the board is free
    '''
    return not board[position]=='#'

def full_board_check(board):
    '''
    Function to check if the board is full
    '''
    for i in range(1,10):
        if space_check(board, i):
            return False
    return True

def player_choice(board):
    '''
    Function to handle player input for choosing positions
    '''
    while True:
        position=input("Enter the position (1-9): ")
        if not position.isdigit():
            print(f"Please enter a digit from 1-9 (You entered: {position}! Try again!")
            continue

        position=int(position)
        if 1 <= position <= 9:
            if not space_check(board,position):
                return position
            else:
                print("Position is already taken! Try another one!")
        else:
            print("Position has to be between 1-9! Try again!")

def replay():
    '''
    Function to handle player input for replaying the game
    '''
    response=input("Do you want to play again? (Y/N): ")
    return response.upper()=="Y"
    #all other responses are considered NO

print('Welcome to Tic Tac Toe!')

def explain_rules():
    '''
    Function to explain the rules of the game
    '''
    board=range(0,10)
    display_board(board)
    print("Above are the positions of the board: ")
    print("\nYou have to get 3 of your markers in a line to win!")

def main():
    '''
    Main function to run the Tic Tac Toe game
    '''
    while True:
        explain_rules()
        game_board=['#']*10
        print("First choose between you who will be X and who will be O.")
        player_marker_x,player_marker_o=player_input()

        turn=choose_first()
        print(f"Player {turn} will go first!")

        while True:
            print(f"Players {turn} turn!")
            player_position = player_choice(game_board)
            player_marker = player_marker_x if turn=="X" else player_marker_o
            place_marker(game_board, player_marker, player_position)
            display_board(game_board)

            if turn=="X":
                if win_check(game_board, player_marker_x):
                    display_board(game_board)
                    print(f"Congratulations Player {turn}! You have won the game!")
                    break
                if full_board_check(game_board):
                    display_board(game_board)
                    print("The game is a draw!")
                    break

            if turn=="O":
                if win_check(game_board, player_marker_o):
                    display_board(game_board)
                    print(f"Congratulations Player {turn}! You have won the game!")
                    break
                if full_board_check(game_board):
                    display_board(game_board)
                    print("The game is a draw!")
                    break

            turn = "O" if turn == "X" else "X"

        if not replay():
            break

main()
