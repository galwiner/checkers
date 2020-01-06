import pprint

import numpy as np

N = 8
BLACK = 2
WHITE = 1
EMPTY = 0
VERBOSE = False
SHOW_BOARD = False
PLAY_BY_PLAY = False


def makeBoard():
    """Returns an empty playing board as a numpy array"""
    board = np.zeros((N, N))
    for ind in range(1, N, 2):
        board[0, ind] = WHITE
        board[1, ind - 1] = WHITE
        board[2, ind] = WHITE
        board[N - 3, ind - 1] = BLACK
        board[N - 2, ind] = BLACK
        board[N - 1, ind - 1] = BLACK
    return board


def parseMoves(file):
    """
    Loads the moves stored in the file and returns them as a numpy array, where every row is a move.
    pos0,pos1 are the source location for the move, pos2,pos3 are the target
    white moves first (first row)
    """
    try:
        with open(file) as f:
            data = np.loadtxt(f, delimiter=",", unpack=False, dtype=int)
            for idx, row in enumerate(data):
                if (abs(row[0] - row[2]) != 1) & (abs(row[0] - row[2]) != 2):
                    # raise IndexError('Bad move in moves file.')
                    raise IndexError(f'Line {idx + 1}  illegal move {row}')
                if (abs(row[1] - row[3]) != 1) & (abs(row[1] - row[3]) != 2):
                    raise IndexError(f'Line {idx + 1}  illegal move {row}')
        return data
    except IndexError:
        raise
    except:
        raise


def isPosEmpty(board, pos):
    """
    Checks if the position indicated in pos is empty. Returns Bool.
    """
    if board[pos[1], pos[0]] == EMPTY:
        return True
    else:
        return False


def isLegalMove(board, move):
    """
    Checks if a move is legal: from a non empty position and to an empty position, and either a 1 or 2 col/row move.
    """
    if isPosEmpty(board, move[0:2]):
        return False
    if not isPosEmpty(board, move[2:4]):
        return False
    if (abs(move[0] - move[2]) != 1) & (abs(move[0] - move[2]) != 2):
        return False
    if (abs(move[1] - move[3]) != 1) & (abs(move[1] - move[3]) != 2):
        return False
    else:
        return True


def hasLegalMoves(board, pos):
    """checks if legal moves remain on the board"""
    if board[pos[0], pos[1]] == EMPTY:
        return False
    if (board[pos[0], pos[1]] == WHITE) & (pos[0] == (N - 1)):
        return False
    if (board[pos[0], pos[1]] == WHITE) & (pos[0] == 0):
        return False
    if (board[pos[0], pos[1]] == WHITE) & (pos[1] == (N - 1)):
        if isPosEmpty(board, [pos[0] + 1, pos[1] - 1]):
            return True
        else:
            return False

    if (board[pos[0], pos[1]] == WHITE) & (pos[1] == 0):
        if isPosEmpty(board, [pos[0] + 1, pos[1] + 1]):
            return True
        else:
            return False

    if (board[pos[0], pos[1]] == BLACK) & (pos[1] == (N - 1)):
        if isPosEmpty(board, [pos[0] - 1, pos[1] - 1]):
            return True
        else:
            return False

    if (board[pos[0], pos[1]] == BLACK) & (pos[1] == 0):
        if isPosEmpty(board, [pos[0] - 1, pos[1] + 1]):
            return True
        else:
            return False

    if board[pos[0], pos[1]] == BLACK:
        if isPosEmpty(board, [pos[0] - 1, pos[1] + 1]):
            return True
        elif isPosEmpty(board, [pos[0] - 1, pos[1] - 1]):
            return True
        else:
            return False

    if board[pos[0], pos[1]] == WHITE:
        if isPosEmpty(board, [pos[0] + 1, pos[1] + 1]):
            return True
        elif isPosEmpty(board, [pos[0] + 1, pos[1] - 1]):
            return True
        else:
            return False


def isGameOver(board):
    """checks if legal moves remain and there are more than one color of board pieces"""
    if (np.sum(board == WHITE) == 0) | (np.sum(board == BLACK) == 0):
        return True
    for ind in range(N):
        for jnd in range(N):
            if hasLegalMoves(board, [ind, jnd]):
                return False
    return True


def getPieceColor(board, pos):
    """get the piece color in pos"""
    return board[pos[0], pos[1]]


def getMoveDir(piece):
    if piece == WHITE:
        mov_dir = 1
    if piece == BLACK:
        mov_dir = -1
    else:
        mov_dir = 0
    return mov_dir


def getEnemyNeighbours(board, pos):
    """get the list of enemies at the current position"""
    piece = getPieceColor(board, pos)
    mov_dir = getMoveDir(piece)
    neighbours = []
    if piece == EMPTY:
        return []
    for ind in [1, -1]:
        try:
            if board[pos[0] + mov_dir, pos[1] + ind] == (3 - piece):
                neighbours.append(np.array((pos[0] + mov_dir, pos[1] + ind)))
                if VERBOSE:
                    print(neighbours)
        except IndexError as e:
            pass
    return neighbours


def isCapture(board, move):
    """Check if the requested move is a capture move"""
    if abs(move[0] - move[2]) == 2:
        if abs(move[1] - move[3]) == 2:
            if VERBOSE:
                print('capture move!')
            return True
        else:
            raise IndexError("Bad capture  move!")
    else:
        return False


def getCaptureCoords(board, move):
    """if the move is a capture, get the coords of the captured piece"""
    if not isCapture(board, move):
        raise AttributeError
    return np.array([(move[2] + move[0]) / 2, (move[3] + move[1]) / 2], dtype=int)


def makeMove(board, move):
    """move the piece and return a new board."""
    new_board = board
    if isPosEmpty(board, move[0:2]):
        raise IndexError('no piece in source position!')
    if not isPosEmpty(board, move[2:4]):
        raise IndexError('Target position is not empty!')
    else:
        piece = new_board[move[1], move[0]]
        new_board[move[1], move[0]] = EMPTY
        new_board[move[3], move[2]] = piece
        if isCapture(board, move):
            cap_coords = getCaptureCoords(board, move)
            if VERBOSE:
                print('piece captured! ' + str(cap_coords))

            new_board[cap_coords[1], cap_coords[0]] = EMPTY
    return new_board


def testWinner(board):
    """check who has more pieces"""
    if np.sum(board == WHITE) > np.sum(board == BLACK):
        return "white wins"
    if np.sum(board == WHITE) < np.sum(board == BLACK):
        return "black wins"
    else:
        return "draw!"


def playGame(file):
    """the main function of the module. gets a file with a list of plays, parses it and then runs the game"""
    try:
        moves = parseMoves(file)
    except Exception as e:
        return e.args[0]

    board = makeBoard()
    for move in moves:
        new_board = makeMove(board, move)
        if SHOW_BOARD:
            showBoard(new_board)
        if PLAY_BY_PLAY:
            keystroke = input("Press enter to show the next move or q and enter to quit.")
            if keystroke == 'q':
                break
        board = new_board
    if VERBOSE:
        print(testWinner(board))
    if isGameOver(board):
        print(testWinner(board))
        return testWinner(board)
    else:
        print("incomplete game")
        return "incomplete game"


def showBoard(board):
    """prints the input board as a textual array"""
    textBoard = [["_" for x in range(N)] for y in range(N)]
    for ind in range(N):
        for jnd in range(N):
            if board[ind, jnd] == BLACK:
                textBoard[ind][jnd] = u"\u25CB"
            elif board[ind, jnd] == WHITE:
                textBoard[ind][jnd] = u"\u25CF"
            else:
                textBoard[ind][jnd] = "_"
    pprint.pprint(textBoard)


if __name__ == "__main__":
    b = makeBoard()
    showBoard(b)
    playGame('illegalEntries.txt')
