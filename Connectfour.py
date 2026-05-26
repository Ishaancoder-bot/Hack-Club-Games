import os

def clear(): os.system('cls' if os.name=='nt' else 'clear')

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, 1, 2
SYMBOLS = {0: ".", 1: "X", 2: "O"}
COLORS  = {1: "\033[91m", 2: "\033[94m", 0: "\033[0m"}
RESET   = "\033[0m"

def new_board():
    return [[EMPTY]*COLS for _ in range(ROWS)]

def draw(board, scores):
    clear()
    print(f"\n  CONNECT FOUR  |  X (P1): {scores[1]}  O (P2): {scores[2]}\n")
    print("  " + "  ".join(str(i) for i in range(COLS)))
    print("  " + "--"*COLS)
    for row in board:
        line = "  "
        for cell in row:
            line += COLORS[cell] + SYMBOLS[cell] + RESET + " "
        print(line)
    print()

def drop(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = player
            return r
    return -1

def check_win(board, player):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i]==player for i in range(4)): return True
    # Vertical
    for r in range(ROWS-3):
        for c in range(COLS):
            if all(board[r+i][c]==player for i in range(4)): return True
    # Diagonal down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i]==player for i in range(4)): return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i]==player for i in range(4)): return True
    return False

def board_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))

def get_move(board, player, name):
    while True:
        try:
            col = int(input(f"  {name} ({SYMBOLS[player]}) — choose column (0-6): "))
            if 0 <= col < COLS and board[0][col] == EMPTY:
                return col
            print("  Invalid or full column!")
        except ValueError:
            print("  Enter a number!")

def play():
    board = new_board()
    scores = {1: 0, 2: 0}
    names = {
        1: input("  Player 1 name (X): ").strip() or "Player 1",
        2: input("  Player 2 name (O): ").strip() or "Player 2"
    }

    while True:
        current = 1
        board = new_board()

        while True:
            draw(board, scores)
            col = get_move(board, current, names[current])
            drop(board, col, current)

            if check_win(board, current):
                draw(board, scores)
                scores[current] += 1
                print(f"  {names[current]} WINS!")
                break

            if board_full(board):
                draw(board, scores)
                print("  It's a draw!")
                break

            current = 2 if current == 1 else 1

        if input("\n  Play again? (yes/no): ").lower() not in ("yes","y"):
            break

play()