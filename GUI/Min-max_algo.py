import chess
from GUI import *
import random
from copy import deepcopy

def random_agent(BOARD):
    return random.choise(list(BOARD.legal_moves))

scoring= {'p': -1,
          'n': -3,
          'b': -3,
          'r': -5,
          'q': -9,
          'k': 0,
          'P': 1,
          'N': 3,
          'B': 3,
          'R': 5,
          'Q': 9,
          'K': 0,
          }

def eval_board(BOARD):
    score = 0
    pieces = BOARD.piece_map()
    for key in pieces:
        score += scoring[str(pieces[key])]

    return score

def MinMaxDepthN(BOARD, N):
    moves = list(BOARD.legal_moves)
    scores = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)

        if N > 1:
            temp_best_move = MinMaxDepthN(temp, N-1)
            temp.push(temp_best_move)
        
    scores.append(temp_best_move)

    if BOARD.turn == True:
        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move


def depth(BOARD):
    depth = input("Please enter the depth of AI you are facing: ")
    return MinMaxDepthN(BOARD, depth)