import pygame
import math
import random
import chess
import chess.polyglot
from copy import deepcopy

#init av skärkm
X = 800 
Y = 800
scrn = pygame.display.set_mode((X,Y))
pygame.init()


#basic färger till brädan
WHITE = (255, 255 ,255) 
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)

#init av brädan 
b = chess.Board()

#pjäser

pieces = {'p': pygame.image.load('b_pawn.png').convert(),
          'n': pygame.image.load('b_knight.png').convert(),
          'b': pygame.image.load('b_bishop.png').convert(),
          'r': pygame.image.load('b_rook.png').convert(),
          'q': pygame.image.load('b_queen.png').convert(),
          'k': pygame.image.load('b_king.png').convert(),
          'P': pygame.image.load('w_pawn.png').convert(),
          'N': pygame.image.load('w_knight.png').convert(),
          'B': pygame.image.load('w_bishop.png').convert(),
          'R': pygame.image.load('w_rook.png').convert(),
          'Q': pygame.image.load('w_queen.png').convert(),
          'K': pygame.image.load('w_king.png').convert(),
          }

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

#Opening book
#reader = chess.polyglot.open_reader('baron30.bin')

def random_agent(BOARD):
    return random.choise(list(BOARD.legal_moves))

def eval_board(BOARD):
    score = 0
    pieces = BOARD.piece_map()
    for key in pieces:
        score += scoring[str(pieces[key])]

    return score

def eval_space(BOARD):
    no_moves = len(list(BOARD.legal_moves))

    value = (no_moves/(20+no_moves))

    if BOARD.turn == True:
        return value
    else:
        return -value

#this is min_max at depth one
def most_value_agent(BOARD):

    moves = list(BOARD.legal_moves)
    scores = []
    for move in moves:
        #creates a copy of BOARD so we dont
        #change the original class
        temp = deepcopy(BOARD)
        temp.push(move)

        scores.append(eval_board(temp))

    if BOARD.turn == True:
        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move

def min_maxN(BOARD,N,status):

    #opening_move = reader.get(BOARD)
    #if opening_move == None:
        #pass
    #else:
        #return opening_move.move


    #generate list of possible moves
    moves = list(BOARD.legal_moves)
    scores = []

    #score each move
    for move in moves:
        #temp allows us to leave the original game state unchanged
        temp = deepcopy(BOARD)
        temp.push(move)

        #here we must check that the game is not over
        outcome = temp.outcome()
        
        #if checkmate
        if outcome == None:
            #if we have not got to the final depth
            #we search more moves ahead
            if N>1:
                #temp_best_move = min_maxN(temp,N-1)
                #temp.push(temp_best_move)
                temp_best_move = alpha_beta(temp, N-1, float('-inf'), float('inf'), status)
                scores.append(temp_best_move)
            else:
                scores.append(eval_board(temp))
        

        #if checkmate
        elif temp.is_checkmate():

            # we return this as best move as it is checkmate
            return move

        # if stalemate
        else:
            #value to disencourage a draw
            #the higher the less likely to draw
            #default value should be 0
            #we often pick 0.1 to get the bot out of loops in bot vs bot
            val = 1000
            if BOARD.turn == True:
                scores.append(-val)
            else:
                scores.append(val)

        #this is the secondary eval function
        scores[-1] = scores[-1] + eval_space(temp)

    if BOARD.turn == True:
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]

    return best_move

def alpha_beta(BOARD, depth, alpha, beta, maximising_player):
    if depth == 0 or BOARD.is_game_over():
        return eval_board(BOARD)
    if maximising_player:
        max_eval = float('-inf')
        for move in BOARD.legal_moves:
            BOARD.push(move)
            eval_score = alpha_beta(BOARD, depth - 1, alpha, beta, False)
            BOARD.pop()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        #print(f"Max evaluation score at depth {depth}: {max_eval}")    
        return max_eval  
    else:
        min_eval = float('inf')
        for move in BOARD.legal_moves:
            BOARD.push(move)
            eval_score = alpha_beta(BOARD, depth - 1, alpha, beta, True)
            BOARD.pop()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        #print(f"Min evaluation score at depth {depth}: {min_eval}")
        return min_eval  


def depth(BOARD):
    depth = 2
    return MinMaxDepthN(BOARD, depth)

def update(scrn,board):

    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            pass
        else:
            scrn.blit(pieces[str(piece)],((i%8)*100,700-(i//8)*100))

    for i in range(7):
        i=i+1
        pygame.draw.line(scrn, WHITE,(0,i*100), (800, i*100))
        pygame.draw.line(scrn, WHITE,(i*100,0),(i*100,800))

    pygame.display.flip()                

############## main för att human vs human
def main(BOARD):
    scrn.fill(BEIGE)
    pygame.display.set_caption('Chess')

    index_moves = []
    moves = []

    status = True
    while (status):
        update(scrn,BOARD)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               status = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                scrn.fill(BEIGE)
                pos = pygame.mouse.get_pos()

                square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                index = (7-square[1])*8+(square[0])

                if index in index_moves:
                    move = moves[index_moves.index(index)]
                    print("Selected move:", move)  # Debugging: Print the selected move
                    if move in BOARD.legal_moves:
                        print("Executing move...")  # Debugging: Confirm that the move is being executed
                        BOARD.push(move)
                        moves = []  # Clear the moves list after executing the move
                        print("Board state after move:")
                        print(BOARD)  # Debugging: Print the board state after the move
                    else:
                        print("Invalid move:", move)  # Debugging: Print if the move is invalid
                    index = None
                    index_moves = []
                        
                else:
                    piece = BOARD.piece_at(index)

                    if piece is None:
                        pass
                    else:
                        all_moves = list(BOARD.legal_moves)
                        print("All legal moves:", all_moves)  # Debugging: Print all legal moves
                        for m in all_moves:
                            if m.from_square == index and m not in moves:  # Check if move is not already in moves
                                moves.append(m)

                                t = m.to_square

                                TX1 = 100 * (t % 8)
                                TY1 = 100 * (7 - t // 8)

                                pygame.draw.rect(scrn, BLUE, pygame.Rect(TX1, TY1, 100, 100), 5)
                                print("Added move:", m)  # Debugging: Print added move
                        index_moves = [a.to_square for a in moves]
                    
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    ##pygame.display.update()    
    pygame.quit()  

def main_one_agent(BOARD, depth, agent_color):
    
    '''
    for agent vs human game
    color is True = White agent
    color is False = Black agent
    '''
    
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
     
        if BOARD.turn==agent_color:
            move = min_maxN(BOARD, 5, status)
            BOARD.push(move)
            scrn.fill(BLACK)

        else:

            for event in pygame.event.get():
         
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #reset previous screen from clicks
                    scrn.fill(BLACK)
                    #get position of mouse
                    pos = pygame.mouse.get_pos()

                    #find which square was clicked and index of it
                    square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                    index = (7-square[1])*8+(square[0])
                    
                    # if we have already highlighted moves and are making a move
                    if index in index_moves: 
                        
                        move = moves[index_moves.index(index)]
                        print(BOARD)
                        print(move)
                        BOARD.push(move)
                        index=None
                        index_moves = []
                        
                    # show possible moves
                    else:
                        
                        piece = BOARD.piece_at(index)
                        
                        if piece == None:
                            
                            pass
                        else:

                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 100*(t%8)
                                    TY1 = 100*(7-t//8)

                                    
                                    pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                            #print(moves)
                            index_moves = [a.to_square for a in moves]
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()

def main_two_agent(BOARD,agent1,agent_color1,agent2):
    '''
    for agent vs agent game
    
    '''
  
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
        if BOARD.turn==agent_color1:
            BOARD.push(agent1(BOARD))

        else:
            BOARD.push(agent2(BOARD))

        scrn.fill(BLACK)
            
        for event in pygame.event.get():
     
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                status = False
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()