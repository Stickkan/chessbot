import pygame
import chess
import math


#init av skärkm
X = 800 
Y = 800
scrn = pygame.display.set_mode((X,Y))
pygame.init()


#basic färger från brädan
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
                    if move in BOARD.legal_moves:
                        print("Board state before move:")
                        print(BOARD)
                        BOARD.push(move)
                        print("Board state before move:")
                        print(BOARD)
                       ## BOARD = BOARD.copy()
                    index=None
                    index_moves = []
                        
                else:
                    piece = BOARD.piece_at(index)

                    if piece == None:
                        pass
                    else:
                        all_moves = list(BOARD.legal_moves)
                        move = []
                        for m in all_moves:
                            if m.from_square == index:
                                moves.append(m)

                                t = m.to_square

                                TX1= 100*(t%8)

                                TY1 = 100*(7-t//8)

                                pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                        index_moves = [a.to_square for a in moves]
                    
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    ##pygame.display.update()    
    pygame.quit()  

def main_one_agent(BOARD,agent,agent_color):
    
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
            BOARD.push(agent(BOARD))
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
                        #print(BOARD)
                        #print(move)
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

main(b)