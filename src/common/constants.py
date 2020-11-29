import random 
import numpy as np

EMPTY = 0
RED = 1
YELLOW = 2

DX = 6
DY = 7
NUMBER_TO_WIN = 4

HASH_CONSTANT = int(random.uniform(0, 2**64))

MAX_LEGAL_MOVES = DY * 2
MAX_PLAYOUT_LEGAL_MOVES = (DY + DX * DY) * 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
SQUARESIZE = 100
RED_COLOR = (255,0,0)
YELLOW_COLOR = (255,255,0)
WHITE = (255, 255, 255)
RADIUS = int(SQUARESIZE/2 - 5)
WIDTH = DY * SQUARESIZE
HEIGHT = (DX+1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

def init_hash_table():
    random.seed(0)
    hash_table = np.zeros((2, DX, DY))
    for i in range(hash_table.shape[0]):
        for j in range(hash_table.shape[1]):
            for k in range(hash_table.shape[2]):
                hash_table[i][j][k] = int(random.uniform(0, 2**64))
    return hash_table

HASH_TABLE = init_hash_table()
