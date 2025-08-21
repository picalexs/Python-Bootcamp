import random

def display_board(board):
    nrOfMarkers=0
    for m in board[1:]:
        nrOfMarkers+=1
        print(f'| {m} ',end="")
        if nrOfMarkers%3==0:
            print('|')
    print('-'*13)

def player_input():
    while True:
        marker=input("Player1 choose marker (X or O): ")
        if marker=="0":
            marker="O"
        marker=marker.upper()
        if marker!="X" and marker!="O":
            print("You have to enter either 'X' or 'O'")
            continue
        if marker=="X":
            return ('X','O')
        else:
            return ('O','X')

def place_marker(board, marker, position):
    board[position]=marker
    
def win_check(board, mark):
    #Has an entire row
    if ((board[1]==mark and board[2]==mark and board[3]==mark)
        or (board[4]==mark and board[5]==mark and board[6]==mark)
        or (board[7]==mark and board[8]==mark and board[9]==mark)):
        return True
    
    #Has an entire column
    if ((board[1]==mark and board[4]==mark and board[7]==mark)
        or (board[2]==mark and board[5]==mark and board[8]==mark)
        or (board[3]==mark and board[6]==mark and board[9]==mark)):
        return True
    
    #Has an entire diagonal
    if ((board[1]==mark and board[5]==mark and board[9]==mark)
        or (board[3]==mark and board[5]==mark and board[7]==mark)):
        return True
    return False

def choose_first():
    first_player=random.randint(0,1)
    if first_player==0:
        return 'X'
    return 'O'

def space_check(board, position):
    return not board[position]=='#'

def full_board_check(board):
    for i in range(1,10):
        if space_check(board, i):
            return False
    return True

def player_choice(board):
    while True:
        position=input("Enter the position (1-9): ")
        if not position.isdigit():
            print(f"Please enter a digit from 1-9 (You entered: {position}! Try again!")
            continue
        
        position=int(position)
        if position>=1 and position<=9:
            if not space_check(board,position):
                return position
            else:
                print("Position is already taken! Try another one!")
        else:
            print("Position has to be between 1-9! Try again!")
           
def replay():
    response=input("Do you want to play again? (Y/N): ")
    return response.upper()=="Y"
    #all other responses are considered NO
    
print('Welcome to Tic Tac Toe!')

def explain_rules():
    board=range(0,10)
    display_board(board)
    print("Above are the positions of the board: ")
    print("\nYou have to get 3 of your markers in a row (horizontally, vertically, or diagonally) to win!")


while True:
    explain_rules()
    board=['#']*10
    print("First choose between you who will be X and who will be O.")
    player_marker_X,player_marker_O=player_input()
    
    turn=choose_first()
    print(f"Player {turn} will go first!")

    while True:
        print(f"Players {turn} turn!")
        position = player_choice(board)
        player_marker = player_marker_X if turn=="X" else player_marker_O
        place_marker(board, player_marker, position)
        display_board(board)
        
        if turn=="X":
            if win_check(board, player_marker_X):
                display_board(board)
                print(f"Congratulations Player {turn}! You have won the game!")
                break
            if full_board_check(board):
                display_board(board)
                print("The game is a draw!")
                break
            
        if turn=="O":
            if win_check(board, player_marker_O):
                display_board(board)
                print(f"Congratulations Player {turn}! You have won the game!")
                break
            if full_board_check(board):
                display_board(board)
                print("The game is a draw!")
                break
        
        turn = "O" if turn == "X" else "X"
        
    if not replay():
        break 