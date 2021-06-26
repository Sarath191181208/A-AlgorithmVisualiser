import json
import os
import pygame
import time
from queue import PriorityQueue
import pygame_gui

# todo must add buttons and fix the color issue
pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((600, 680))
pygame.display.set_caption('A* visualiser')
FPS = 20

manager = pygame_gui.UIManager((600, 680))
background = pygame.Surface((600, 680))
background.fill(pygame.Color('#000000'))


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
CYAN = (100, 210, 180)
YELLOW = (225, 235, 70)
AMBER = (220, 0, 50)
TRANSPARENT = (0, 0, 0, 0)

checksClr = BLUE
boardClr = WHITE
txtClr = GREAY
startClr = ORANGE
endClr = GREEN
obstacleClr = BLACK
pathClr = VIOLET


translationFactor = 0

# todo rotation of arrow : mouse hint/tooltip    -> https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjy9PrnxbPxAhXFW3wKHeLcC5QQFnoECAIQAA&url=https%3A%2F%2Fpygame-gui.readthedocs.io%2Fen%2Flatest%2Fpygame_gui.elements.html&usg=AOvVaw2pKZFNKauew3F4V-9vsAVg


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
        WIN.blit(background, (0, 0))
        if win == None:
            win = WIN
        win.fill(BLACK)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),
                             (self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0),
                             (colGap*i, self.width), thick)
        self.help_bar()
        pygame.display.update()

    def clicked(self, pos):
        x, y = pos
        if x >= self.rows or y >= self.cols or x < 0:
            return -1

        if self.start == None and self.cubes[x][y].colour == WHITE:
            self.cubes[x][y].colour = startClr
            self.start = self.cubes[x][y]
            self.cubes[x][y].placed = True

        elif self.end == None and self.cubes[x][y].colour == WHITE:
            self.cubes[x][y].colour = endClr
            self.end = self.cubes[x][y]
            self.cubes[x][y].placed = True

        elif self.cubes[x][y].colour == WHITE:
            self.cubes[x][y].colour = obstacleClr
            self.cubes[x][y].placed = True

        self.draw()

    def a_star(self):
        count = 0
        open_set = PriorityQueue()
        # open_set[2] : class(Cube)
        open_set.put((0, count, self.start))
        came_from = {}
        # key : cube
        g_score = {cube: float("inf") for row in self.cubes for cube in row}
        g_score[self.start] = 0
        # key : cube
        f_score = {spot: float("inf") for row in self.cubes for spot in row}
        f_score[self.start] = h(self.start.get_pos(), self.end.get_pos())
        # cube
        open_set_hash = {self.start}
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end:
                self.reconstruct_path(came_from)
                return True
            for neighbour in current.neighbours:
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + \
                        h(neighbour.get_pos(), self.end.get_pos())
                    if not (neighbour in open_set_hash):
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.update_colour(CYAN)

                        # neighbor.make_open()
                        self.draw()
            if current != self.start:
                current.update_colour(TURTLEGREEN)

        return False

    def reset(self):
        self.start = None
        self.end = None
        self.create_board()
        self.draw()

    def reconstruct_path(self, came_from):
        current = self.end
        while current in came_from:
            # time.sleep(0.3)
            current = came_from[current]
            current.update_colour(pathClr)
            self.draw()

    def delete(self, x, y):
        self.cubes[x][y].placed = False
        self.cubes[x][y].colouring = False
        self.cubes[x][y].colour = WHITE
        if self.cubes[x][y] == self.start:
            self.start = None
        elif self.cubes[x][y] == self.end:
            self.end = None
        self.draw()

    def help_bar(self):
        text = ""
        postfix = "block"
        if self.start == None:
            text = "start"
        elif self.end == None:
            text = "end"
        else:
            text = "walls"
            postfix = ''
        txt = PYtxt(f'place the {text} {postfix}', 22)
        WIN.blit(txt, (20, self.height+txt.get_height()))

        x, y = 320, self.height + txt.get_height()
        text = PYtxt("L", 16)
        WIN.blit(text, (x, y))
        clickTxt = PYtxt('left click for inserting', 11)
        WIN.blit(clickTxt,
                 (x-clickTxt.get_width()*0.8, y-text.get_height()))
        pygame.draw.rect(WIN, (0, 0, 0),
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)

        x, y = 360, self.height + txt.get_height()
        text = PYtxt("R", 16)
        clickTxt = PYtxt('right click for deleting', 11)
        WIN.blit(clickTxt,
                 (x-clickTxt.get_width()*0.7, y+text.get_height()+6))
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, (0, 0, 0),
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)

        x, y = 430, self.height + txt.get_height()
        text = PYtxt("S", 16)
        clickTxt = PYtxt('space to start', 11)
        WIN.blit(clickTxt,
                 (x-clickTxt.get_width()*0.7, y-text.get_height()))
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, (0, 0, 0),
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)

        x, y = 480, self.height + txt.get_height()
        text = PYtxt("r", 16)
        clickTxt = PYtxt('r key to reset', 11)
        WIN.blit(clickTxt,
                 (x-clickTxt.get_width()*0.7, y+text.get_height()+6))
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, (0, 0, 0),
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)

        x, y = 520, self.height + txt.get_height()
        text = PYtxt("s", 16)
        clickTxt = PYtxt('s key to save', 11)
        WIN.blit(clickTxt,
                 (x-clickTxt.get_width()*0.7, y-text.get_height()))
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, (0, 0, 0),
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)

        x, y = 560, self.height + txt.get_height()
        text = PYtxt("o", 16)
        clickTxt = PYtxt(' o to load saved', 11)
        WIN.blit(clickTxt,
                 (x-clickTxt.get_width()*0.7, y+text.get_height()+6))
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, (0, 0, 0),
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)


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
        self.placed = False
        self.neighbours = []
        self.colouring = False

    def draw(self, win):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        # if self.colour == WHITE:
        #     pygame.draw.rect(win, self.colour,
        #                      pygame.Rect(x+3, y+3, colGap-5, rowGap-5))
        if not self.placed:
            if self.colouring:
                pygame.draw.rect(win, WHITE,
                                 pygame.Rect(x, y, colGap, rowGap))
            pygame.draw.rect(win, self.colour,
                             pygame.Rect(x+3, y+3, colGap-5, rowGap-5))
            # pygame.draw.rect(win, self.colour,
            #                  pygame.Rect(x, y, colGap, rowGap))
        else:
            pygame.draw.rect(win, self.colour,
                             pygame.Rect(x, y, colGap, rowGap))

        # if self.value == 1:
        #newImg = pygame.transform.scale(queenImg, (int(colGap-self.centerFactor), int(rowGap-self.centerFactor)))
        #win.blit(newImg, (x+self.centerFactor/2, y+self.centerFactor/2))

        if self.colour == startClr:
            # 14 = 21
            text = PYtxt(">", int(1.3 * rowGap), pygame.font.match_font(
                'consolas', bold=True, italic=False))
            win.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))
        if self.colour == endClr:
            txt = PYtxt("O", int(1.3 * rowGap), pygame.font.match_font(
                'callibri', bold=False, italic=False))
            WIN.blit(txt, (x + (colGap/2 - txt.get_width()/2),
                           y + (rowGap/2 - txt.get_height()/2)))
            # WIN.blit(text, (x + (colGap/2 - text.get_width()/2),
            # y + (rowGap/2 - text.get_height()/2) - txt.get_height()/4 - 0.5))

    def get_pos(self):
        return (self.row, self.col)

    def update_neighbours(self, grid):
        self.neighbours = []
        # DOWN
        if self.row < self.rows - 1 and not grid.cubes[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid.cubes[self.row + 1][self.col])

        if self.row > 0 and not grid.cubes[self.row - 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid.cubes[self.row - 1][self.col])

        # RIGHT
        if self.col < self.rows - 1 and not grid.cubes[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid.cubes[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid.cubes[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid.cubes[self.row][self.col - 1])

    def is_barrier(self):
        return self.colour == obstacleClr

    def update_colour(self, colour):
        if not (self.colour == startClr or self.colour == endClr):
            self.colouring = True
            self.colour = colour


board = Grid(20, 20, WIN.get_width(), WIN.get_width())
board.draw()
run = True
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 600), (100, 50)),
                                            text='Say Hello',
                                            manager=manager, tool_tip_text="animations")

while run:

    clock.tick(FPS)
    time_delta = clock.tick(FPS)/1000.0
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        y -= translationFactor
        board.clicked((y, x))
    elif pygame.mouse.get_pressed()[2]:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.delete(y, x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and board.start and board.end:
                for row in board.cubes:
                    for spot in row:
                        spot.update_neighbours(board)
                board.a_star()
            if event.key == pygame.K_r:
                board.reset()
            # save and load
            if event.key == pygame.K_s:
                if not os.path.exists('./saveBoard.json'):
                    with open('./saveBoard.json', 'a') as outfile:
                        json_object = json.dumps({})
                        outfile.write(json_object)
                with open('./saveBoard.json', 'r+') as outfile:
                    boardState = {}
                    boardState['board'] = {}
                    helperDic = {}
                    for row in board.cubes:
                        for cube in row:
                            if cube.colour == obstacleClr:
                                x, y = cube.get_pos()
                                key = str(x)+','+str(y)
                                helperDic[key] = cube.colour
                    boardState['board'][0] = helperDic
                    boardState['board'][1] = board.start.get_pos()
                    boardState['board'][2] = board.end.get_pos()
                    boardState['board']['rows'] = board.rows
                    boardState['board']['cols'] = board.cols
                    # outfile.write(json_object)

                    file_data = json.load(outfile)
                    outfile.seek(0, 0)
                    outfile.truncate()
                    file_data.update(boardState)
                    outfile.write(json.dumps(file_data, indent=4))

            if event.key == pygame.K_o:
                if os.path.exists('./saveBoard.json'):
                    data = json.load(open('./saveBoard.json'))
                    data = data['board']
                    if board.rows == data['rows'] and board.cols == data['cols']:
                        board.reset()

                        x, y = data['1'][0], data['1'][1]
                        board.start = board.cubes[x][y]
                        board.cubes[x][y].colour = startClr
                        board.cubes[x][y].placed = True

                        x, y = data['2'][0], data['2'][1]
                        board.end = board.cubes[x][y]
                        board.cubes[x][y].colour = endClr
                        board.cubes[x][y].placed = True

                        for items in data['0']:
                            items = items.split(',')
                            x = int(items[0])
                            y = int(items[1])
                            board.cubes[x][y].colour = obstacleClr
                            board.cubes[x][y].placed = True

                        board.draw()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')
        manager.process_events(event)
    manager.update(time_delta)

    manager.draw_ui(WIN)
    pygame.display.update()


pygame.quit()
