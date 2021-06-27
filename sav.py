# used for saving
import json
import os
# ---------
import time
import pygame
# used in a# algorithm
from queue import PriorityQueue
# used for buttons
import pygame_gui

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((600, 680))
pygame.display.set_caption('A* visualiser')
FPS = 20
manager = pygame_gui.UIManager((600, 680), 'themePygame_gui.json')

# TODO:  animation of some stuff

# return from a simple text to pygame text object


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

# returns the distance heirustic between two points used in algorithm


def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2-x1) + abs(y2-y1)

# saves the board and other things in json


def save():
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

        file_data = json.load(outfile)
        outfile.seek(0, 0)
        outfile.truncate()
        file_data.update(boardState)
        outfile.write(json.dumps(file_data, indent=4))

# loads the saved json if it exists


def load():
    if os.path.exists('./saveBoard.json'):
        data = json.load(open('./saveBoard.json'))
        data = data['board']
        if board.rows == data['rows'] and board.cols == data['cols']:
            # board clear has a property noAnimation which doesnt play animation
            board.clear(True)

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
            # this is because we have to update cube at dark mode its not needed in light  because the  animation plays again
            board.animation()
            board.draw()


def help_bar():
    text = ""
    postfix = "block"
    if board.start == None:
        text = "start"
    elif board.end == None:
        text = "end"
    else:
        text = "walls"
        postfix = ''
    txt = PYtxt(f'place the {text} {postfix}', 16, fontColour=textClr)
    y = 660
    x = 10
    gap = 10
    WIN.blit(txt, (x, y))
    x += txt.get_width() + 2*gap
    y += 5

    txt = PYtxt('1) left click for insert', 11, fontColour=helperTxtClr)
    WIN.blit(txt, (x, y))
    x += txt.get_width() + 2*gap

    txt = PYtxt('2) right click to delete', 11, fontColour=helperTxtClr)
    WIN.blit(txt, (x, y))
    x += txt.get_width() + gap + 100

    # shows the box 'N' if show numbers is true
    y -= 5
    if board.show_numbers:
        text = PYtxt("N", 16, fontColour=helperTxtClr)
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, textClr,
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)


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


boardClr = WHITE
textClr = WHITE if boardClr == BLACK else absBlack
helperTxtClr = GREAY
startClr = ORANGE
endClr = GREEN
obstacleClr = (160, 160, 160, 0.8)
pathClr = VIOLET
gridClr = (160, 160, 160, 0.8)


def toggleTheme(clr):
    if clr == WHITE:
        # return(BLACK, WHITE, (120, 120, 120))
        return BLACK
    else:
        # return(WHITE, absBlack, GREAY)
        return WHITE


translationFactor = 0


class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400):
        self.rows = cols
        self.cols = rows
        # board is saved  here as a 2D array
        self.cubes = None
        self.width = width
        self.height = height
        # used for algorithm
        self.start = None
        self.end = None
        # -------

        # used to show number
        self.show_numbers = False

        # creates self.cubes as like a 2D array
        self.create_board()

    def create_board(self, grid: tuple = (4, 4)) -> list[int]:
        self.cubes = [
            [Cube(None, i, j, self.width, self.height, self.cols, self.rows)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def draw(self, win=None):
        if win == None:
            win = WIN
        win.fill(boardClr)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols

        # this draws cubes onto the screen
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].show_numbers = self.show_numbers
                self.cubes[i][j].draw(win)

        # this draws horizontal lines
        thick = 1
        for i in range(self.rows+1):
            if boardClr == WHITE:
                pygame.draw.line(win, gridClr, (0, i*rowGap),
                                 (self.height, rowGap*i), thick)
        # this draws vertical lines
        for i in range(self.cols+1):
            if boardClr == WHITE:
                pygame.draw.line(win, gridClr, (i*colGap, 0),
                                 (colGap*i, self.width), thick)

        pygame.display.update()

    def animation(self):
        # linearly interpolating animate variable from o to possibly higher than 1
        win = WIN
        win.fill(boardClr)
        # animation for  dark theme
        if boardClr == BLACK:
            for row in self.cubes:
                for cube in row:
                    cube.update()
            return
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        animate = 0.001
        while(True):
            for i in range(self.rows+1):
                pygame.draw.line(win, gridClr, (0, i*rowGap),
                                 (self.height*animate, rowGap*i), 1)
            for i in range(self.cols+1):
                pygame.draw.line(win, gridClr, (i*colGap, 0),
                                 (colGap*i, self.width*animate), 1)
            animate += 0.00075
            if animate >= 1:
                break

            pygame.display.update()

    # checks for  clicked position and returns -1 if its out of  bounds
    def clicked(self, pos):
        # pygame.display.update()
        x, y = pos
        if x >= self.rows or y >= self.cols or x < 0:
            self.draw()
            return -1
        # if  no  start
        if self.start == None and self.cubes[x][y].colour == WHITE:
            self.cubes[x][y].colour = startClr
            self.start = self.cubes[x][y]
            self.cubes[x][y].placed = True

        # if no end
        elif self.end == None and self.cubes[x][y].colour == WHITE:
            self.cubes[x][y].colour = endClr
            self.end = self.cubes[x][y]
            self.cubes[x][y].placed = True

        # end and start  are present
        elif self.cubes[x][y].colour == WHITE:
            self.cubes[x][y].colour = obstacleClr
            self.cubes[x][y].placed = True
        self.cubes[x][y].clickAnimation()
        # self.draw()

    def a_star(self):
        # traverses cubes and updates neighbours
        # we can also do the update at  the time of  placing
        for row in self.cubes:
            for cube in row:
                cube.update_neighbours(self)

        # count is kinda basically score of best path
        count = 0
        # open set stores finalscore , count , cube object
        open_set = PriorityQueue()

        # open_set[2] : class(Cube)
        open_set.put((0, count, self.start))

        # keeps track where  we came from
        came_from = {}

        # key : cube
        g_score = {cube: float("inf") for row in self.cubes for cube in row}
        g_score[self.start] = 0

        # key : cube
        f_score = {spot: float("inf") for row in self.cubes for spot in row}
        f_score[self.start] = h(self.start.get_pos(), self.end.get_pos())

        # cube is saved in hash
        open_set_hash = {self.start}

        while not open_set.empty():
            # this is to quit  even in while loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # gets the cube current = cube
            current = open_set.get()[2]
            # removes cube from possibilities
            open_set_hash.remove(current)

            # if we reached end
            if current == self.end:
                self.reconstruct_path(came_from)
                return True

            # go trough each neighbour untill finding  an end
            for neighbour in current.neighbours:
                temp_g_score = g_score[current] + 1

            # updating/entering f score if its useful
                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + \
                        h(neighbour.get_pos(), self.end.get_pos())

                    # putting the  neighbour to  traverse while loop
                    if not (neighbour in open_set_hash):
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                    # updating  the  neighbour for  animation
                        neighbour.update_colour(CYAN, f_score[neighbour])

            if current != self.start:
                current.update_colour(TURTLEGREEN)

        return False

    def reset(self):
        for row in self.cubes:
            for cube in row:
                if cube.placed == False:
                    cube.reset()
                    cube.update()
        board.draw()

    def clear(self, noAnimation=False):
        count = 0
        for row in self.cubes:
            for cube in row:
                if cube.colour != WHITE:
                    count += 1
                cube.reset()
                cube.update()
        self.start = None
        self.end = None
        self.create_board()
        if count < 10 and not noAnimation:
            self.animation()
        self.draw()

    def reconstruct_path(self, came_from):
        current = self.end
        while current in came_from:

            current = came_from[current]
            current.update_colour(pathClr)
            current.clickAnimation(3)

    def delete(self, x, y):
        if x >= self.rows or y >= self.cols or x < 0:
            self.draw()
            return -1
        self.cubes[x][y].reset()
        self.draw()
        if self.cubes[x][y] == self.start:
            self.start = None
        elif self.cubes[x][y] == self.end:
            self.end = None


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows):
        # used for showing numbers
        self.value = value

        self.row = row
        self.col = col

        # this is the total width and height of the grid not the cube
        self.width = width
        self.height = height

        # useful for later caluculations the total rows and cols
        self.cols = cols
        self.rows = rows

        # useful for animations
        self.colour = WHITE

        # useful for checking if user has placed : used for animations
        self.placed = False

        # neighbouring cubes used in search / algorithm
        self.neighbours = []

        # useful for programm to animate
        self.colouring = False

        # used to toggle view numbers ie the value in algo
        self.show_numbers = False

    def draw(self, win):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap

        # this block of if-else draws a block on to screen
        if not self.placed:
            # this {if} is for dark theme only , boardClr represents the theme
            if self.colouring and boardClr == BLACK:
                pygame.draw.rect(win, WHITE,
                                 pygame.Rect(x-1, y-1, colGap-1, rowGap-1))
            pygame.draw.rect(win, self.colour,
                             pygame.Rect(x+3, y+3, colGap-5, rowGap-5))
        else:
            pygame.draw.rect(win, self.colour,
                             pygame.Rect(x, y, colGap, rowGap))

        # if this cube is start draw {>} onto the plane ie on cube
        if self.colour == startClr:
            text = PYtxt(">", int(1.3 * rowGap), pygame.font.match_font(
                'consolas', bold=True, italic=False))
            win.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))

        # if this cube is end draw {O} onto the plane ie on cube
        # if self.colour == endClr:
        #     txt = PYtxt("O", int(1.3 * rowGap), pygame.font.match_font(
        #         'callibri', bold=False, italic=False))
        #     WIN.blit(txt, (x + (colGap/2 - txt.get_width()/2),
        #                    y + (rowGap/2 - txt.get_height()/2)))

    # drawing numbers
        if not self.value == None and self.show_numbers:
            text = PYtxt(str(self.value), int(rowGap*0.4), pygame.font.match_font(
                'consolas', bold=False, italic=False))
            win.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))

    def update(self):
        self.draw(WIN)
        pygame.display.update()

    def get_pos(self):
        return (self.row, self.col)

    def update_neighbours(self, grid):
        # you can also add diagonal movement here
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

    # used for animating in algo
    def update_colour(self, colour, value=None):
        if not (self.colour == startClr or self.colour == endClr):
            self.colouring = True
            self.colour = colour
            if not value == None:
                self.value = value
        self.update()

    def reset(self):
        self.placed = False
        self.colouring = False
        self.colour = WHITE
        self.value = None
        if boardClr == BLACK:
            rowGap = self.height / self.rows
            colGap = self.width / self.cols
            x = self.col * colGap
            y = self.row * rowGap
            pygame.draw.rect(WIN, BLACK,
                             pygame.Rect(x-1, y-1, colGap-1, rowGap-1))

    def clickAnimation(self, sub=0):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        width = colGap - 10 - sub
        while True:
            width += 0.05
            pygame.draw.rect(WIN, self.colour,
                             pygame.Rect(x+(colGap-width)/2, y+(colGap-width)/2, width, width))
            pygame.display.update()
            if width >= colGap:
                break

        self.draw(WIN)


board = Grid(30, 30, WIN.get_width(), WIN.get_width())
board.animation()
board.draw()

Widgetsbackground = pygame.Surface(
    (board.width, WIN.get_height()-board.height))
Widgetsbackground.fill(boardClr)

# putting buttons relative to each other
gap = 18
start = 40
y = 612
n = 0
reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*gap, y), (60, 40)),
                                            text=f'Reset',
                                            manager=manager, tool_tip_text="Reset the board    ( r : key )")
start += 60
n += 1
toggleNumber_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*gap, y), (60, 40)),
                                                   text=f'Num',
                                                   manager=manager, tool_tip_text="Toggle the show numbers ( n : key )")
start += 60
n += 1
toggleTheme_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*gap, y), (60, 40)),
                                                  text='Theme',
                                                  manager=manager, tool_tip_text="Toggle the theme    ( t : key )")
start += 60
n += 1
run_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*gap, y), (60, 40)),
                                          text='Start',
                                          manager=manager, tool_tip_text="start the visualisation (space : key)")
start += 60
n += 1
clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*gap, 612), (60, 40)),
                                            text='Clear',
                                            manager=manager, tool_tip_text="clear the board or   (c : key)")
start += 60
n += 1
save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*gap, 612), (60, 40)),
                                           text='Save',
                                           manager=manager, tool_tip_text="saves the board or   (s : key)")
start += 60
n += 1
load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start + n * gap, 612), (60, 40)),
                                           text='Load',
                                           manager=manager, tool_tip_text="loads the saved board or (l : key)")


run = True

while run:

    clock.tick(FPS)
    time_delta = clock.tick(FPS)/1000.0

    # checks for left click
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        y -= translationFactor
        board.clicked((y, x))

    # checks for right click
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
                board.reset()
                board.a_star()

            if event.key == pygame.K_c:
                board.clear()

            if event.key == pygame.K_s:
                if board.start and board.end:
                    save()

            if event.key == pygame.K_l:
                load()

            if event.key == pygame.K_r:
                board.reset()

            if event.key == pygame.K_n:
                board.show_numbers = not board.show_numbers
                board.draw()

            if event.key == pygame.K_t:
                boardClr = toggleTheme(boardClr)
                board.animation()
                board.draw()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == clear_button:
                    board.clear()

                if event.ui_element == save_button:
                    if board.start and board.end:
                        save()

                if event.ui_element == load_button:
                    load()

                if event.ui_element == run_button:
                    if board.start and board.end:
                        board.reset()
                        board.a_star()

                if event.ui_element == toggleTheme_button:
                    boardClr = toggleTheme(boardClr)
                    board.animation()
                    board.draw()

                if event.ui_element == toggleNumber_button:
                    board.show_numbers = not board.show_numbers
                    board.draw()

                if event.ui_element == reset_button:
                    board.reset()

        manager.process_events(event)
    manager.update(time_delta)

    WIN.blit(Widgetsbackground, (0, board.height+10))
    # this help_bar shows info of the board
    help_bar()
    manager.draw_ui(WIN)
    pygame.display.update()


pygame.quit()
