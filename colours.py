import pygame
# colours
WHITE = pygame.Color('#d7d7d7')
GREAY = pygame.Color('#464646')
BLACK = pygame.Color('#3c3c3c')
GREEN = pygame.Color('#1eb464')
TURTLEGREEN = pygame.Color('#50c85a')
VIOLET = pygame.Color('#9632dc')
ORANGE = pygame.Color('#dc7832')
CYAN = pygame.Color('#64d2b4')
BLUE = pygame.Color('#03Abfc')
YELLOW = pygame.Color('#ffeb00')
absBlack = pygame.Color('#000000')
RED = pygame.Color('#f00050')


boardClr = WHITE
textClr = WHITE if boardClr == BLACK else absBlack
helperTxtClr = GREAY
startClr = ORANGE
endClr = GREEN
obstacleClr = (160, 160, 160, 0.8)
pathClr = VIOLET
gridClr = (160, 160, 160, 0.8)
