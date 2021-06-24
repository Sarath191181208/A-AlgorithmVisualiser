import pygame
import time
from queue import PriorityQueue

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('A* visualiser')
FPS = 20


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2-x1) + abs(y2-y1)


# WIN.blit(PYtxt('Solved'), (20, 560) -> position)
# pygame.display.update()
# win.blit(text, (x + (colGap/2 - text.get_width()/2),
#                 y + (rowGap/2 - text.get_height()/2)))
WHITE = (215, 215, 215)
GREAY = (70, 70, 70)
BLACK = (60, 60, 60)
BLUE = (10, 40, 100)
GREEN = (30, 180, 100)
TURTLEGREEN = (80, 200, 90)
VIOLET = (150, 50, 220)
ORANGE = (220, 120, 50)
PINK = (250, 160, 160)
CYAN = (30, 210, 180)
YELLOW = (255, 235, 0)
AMBER = (220, 0, 50)
TRANSPARENT = (0, 0, 0, 0)

checksClr = BLUE
boardClr = WHITE
txtClr = GREAY
startClr = ORANGE
endClr = GREEN
obstacleClr = BLACK


translationFactor = 0


class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400):
        self.rows = cols
        self.cols = rows
        self.cubes = None
        self.width = width
        self.height = height
        self.start = None
        self.end = None
        self.create_board()

    def create_board(self, grid: tuple = (4, 4)) -> list[int]:
        self.cubes = [
            [Cube(0, i, j, self.width, self.height, self.cols, self.rows)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def draw(self, win=None):
        if win == None:
            win = WIN
        win.fill(boardClr)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win, self.start, self.end)
        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),
                             (self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0), (colGap*i, self.width))
        pygame.display.update()

    def clicked(self, pos):
        x, y = pos
        if x >= self.rows or y >= self.cols or x < 0:
            return -1
        if self.start == None:
            self.cubes[x][y].colour = startClr
            self.start = (x, y)
        elif self.end == None:
            if (x, y) != self.start:
                self.cubes[x][y].colour = endClr
                self.end = (x, y)
        else:
            if not (pos == self.start or pos == self.end):
                self.cubes[x][y].colour = obstacleClr

        self.draw()


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.centerFactor = 10
        self.colour = WHITE

    def draw(self, win, start=None, end=None):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        pygame.draw.rect(win, self.colour,
                         pygame.Rect(x, y, colGap, rowGap))
        # if self.value == 1:
        #newImg = pygame.transform.scale(queenImg, (int(colGap-self.centerFactor), int(rowGap-self.centerFactor)))
        #win.blit(newImg, (x+self.centerFactor/2, y+self.centerFactor/2))
        if (self.row, self.col) == start:
            # candara consolinas
            text = PYtxt(">", 21, pygame.font.match_font(
                'consolas', bold=True, italic=False))
            win.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))
        if (self.row, self.col) == end:
            txt = PYtxt("O", 28, pygame.font.match_font(
                'callibri', bold=False, italic=False))
            text = PYtxt(".", 28, pygame.font.match_font(
                'callibri', bold=False, italic=False))
            WIN.blit(txt, (x + (colGap/2 - txt.get_width()/2),
                           y + (rowGap/2 - txt.get_height()/2)))
            WIN.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2) - txt.get_height()/4 - 0.5))


board = Grid(20, 20, WIN.get_width(), WIN.get_width())
board.draw()
start = None
run = True
while run:
    clock.tick(FPS)
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        y //= board.width // board.cols
        x //= board.width // board.rows
        y -= translationFactor
        board.clicked((y, x))
        time.sleep(0.3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
