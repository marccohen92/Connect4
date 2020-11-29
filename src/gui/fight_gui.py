import pygame
import math
import numpy as np
from time import sleep
from src.common.constants import DX, DY, RED, YELLOW, SQUARESIZE, BLUE, BLACK, RADIUS, RED_COLOR, YELLOW_COLOR, WIDTH, HEIGHT, SIZE
from src.game.move import Move
from src.game.board import Board

def play_with_gui(p1, p1_table, p2, p2_table, nb_playouts=1000):
    board = Board()
    if p1_table:
        transpositionT1 = {}
    if p2_table:
        transpositionT2 = {}
    board = Board()
    screen = pygame.display.set_mode(SIZE)
    draw_board(board.board, screen)
    pygame.display.update()
    
    quit = False
    while not quit:
        
        if ((board.turn == RED) and (p1 == "manual_move")) or ((board.turn == YELLOW) and (p2 == "manual_move")):
        
            for event in pygame.event.get():

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    if board.turn == RED:
                        pygame.draw.circle(screen, RED_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
                    else: 
                        pygame.draw.circle(screen, YELLOW_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    move = Move(board.turn, col)
                    board.play(move)

                draw_board(board.board, screen)
        else:
            if board.turn == RED:
                if p1_table:
                    move = getattr(board, p1)(nb_playouts, transpositionT1)
                else :
                    move = getattr(board, p1)(nb_playouts)
            elif board.turn == YELLOW:
                if p2_table:
                    move = getattr(board, p2)(nb_playouts, transpositionT2)
                else :
                    move = getattr(board, p2)(nb_playouts)
            board.play(move)
        
        for event in pygame.event.get():
        
            if board.finished:
                draw_board(np.full((DX, DY), board.winner), screen)
                
            if event.type == event.type == pygame.MOUSEBUTTONDOWN:
                draw_board(board.board, screen)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit = True
    

def draw_board(board, screen):
    for c in range(DY):
        for r in range(DX):
            loc_size = (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(screen, BLUE, loc_size)
            loc = (int((c+0.5)*SQUARESIZE), int((r+1.5)*SQUARESIZE))
            pygame.draw.circle(screen, BLACK, loc, RADIUS)

    for c in range(DY):
        for r in range(DX):
            if board[r][c] == RED:
                loc = (int((c+0.5)*SQUARESIZE), int((r+1.5)*SQUARESIZE))
                pygame.draw.circle(screen, RED_COLOR, loc, RADIUS)
            elif board[r][c] == YELLOW: 
                loc = (int((c+0.5)*SQUARESIZE), int((r+1.5)*SQUARESIZE))
                pygame.draw.circle(screen, YELLOW_COLOR, loc, RADIUS)
    pygame.display.update()
    
  