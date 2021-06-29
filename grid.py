import random
import collections
from queue import PriorityQueue
from colours import *
import pygame
themeColour = None


def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2-x1) + abs(y2-y1)

# return from a simple text to pygame text object


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400, WIN=None):
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
        # this is where we draw
        self.WIN = WIN

        # used to show number
        self.show_numbers = False

        self._dir_one = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1)
        ]
        self._dir_two = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]

        self._range = list(range(4))
        self.maze = [[0 for i in range(self.rows)]
                     for j in range(self.cols)]
        self.colour = boardClr
        global themeColour
        themeColour = self.colour
        self.surface = pygame.Surface(
            (self.width, self.height))
        self.surface.fill(self.colour)

        # creates self.cubes as like a 2D array
        self.create_board()

    @property
    def _random(self):
        """Returns a random range to iterate over."""
        random.shuffle(self._range)
        return self._range

    def _create_walk(self, x, y):
        """Randomly walks from one pointer within the maze to another one."""
        for idx in self._random:  # Check adjacent cells randomly
            tx, ty = self._dir_two[idx](x, y)
            # Check if unvisited
            if not self._out_of_bounds(tx, ty) and self.maze[tx][ty] == 0:

                self.maze[tx][ty] = self.maze[self._dir_one[idx](
                    x, y)[0]][self._dir_one[idx](x, y)[1]] = 1  # Mark as visited
                return tx, ty  # Return new cell

        return None, None  # Return stop values

    def _out_of_bounds(self, x, y):
        """Checks if indices are out of bounds."""
        return x < 0 or y < 0 or x >= self.rows or y >= self.cols

    def create_board(self, grid: tuple = (4, 4)) -> list[int]:
        self.cubes = [
            [Cube(None, i, j, self.width, self.height, self.cols, self.rows, self.WIN)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def _create_backtrack(self, stack):
        """Backtracks the stack until walking is possible again."""
        while stack:
            x, y = stack.pop()
            for direction in self._dir_two:  # Check adjacent cells
                tx, ty = direction(x, y)
                # Check if unvisited
                if not self._out_of_bounds(tx, ty) and self.maze[tx][ty] == 0:
                    return x, y  # Return cell with unvisited neighbour

        return None, None  # Return stop values if stack is empty

    def _recursive_backtracking(self):
        """Creates a maze using the recursive backtracking algorithm."""
        self.reset()
        if self.start != None:
            x, y = self.start.get_pos()
            self.maze[x][y] = 1
        if self.end != None:
            x, y = self.end.get_pos()
            self.maze[x][y] = 1
        stack = collections.deque()  # List of visited cells [(x, y), ...]

        x = random.randint(0, self.rows - 1)
        y = random.randint(0, self.cols - 1)
        self.maze[x][y] = 1  # Mark as visited

        while x and y:
            while x and y:
                # this stack is useful for backtracking
                stack.append((x, y))
                # _create_walk enters into x,y and return a new neighbour
                x, y = self._create_walk(x, y)
            # back_track pops the stack untill it finds a route back returns a new neighbour
            x, y = self._create_backtrack(stack)

        for i in range(len(self.maze)):
            for j in range(len(self.maze)):
                if not self.maze[i][j]:
                    self.cubes[i][j].clicked()

    def draw(self):
        '''draws/updates the board onto the screen '''

        win = self.WIN
        win.blit(self.surface, (0, 0))

        rowGap = self.height / self.rows
        colGap = self.width / self.cols

        # this draws cubes onto the screen
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].show_numbers = self.show_numbers
                self.cubes[i][j].draw()

        # this draws horizontal lines
        thick = 1
        for i in range(self.rows+1):
            if self.colour == WHITE:
                pygame.draw.line(win, gridClr, (0, i*rowGap),
                                 (self.height, rowGap*i), thick)
        # this draws vertical lines
        for i in range(self.cols+1):
            if self.colour == WHITE:
                pygame.draw.line(win, gridClr, (i*colGap, 0),
                                 (colGap*i, self.width), thick)

        pygame.display.update()

    def animation(self):
        '''animation of the board'''
        # linearly interpolating animate variable from o to possibly higher than 1
        win = self.WIN
        win.blit(self.surface, (0, 0))
        # animation for  dark theme
        if self.colour == BLACK:
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
        '''clicks at a position
        :param pos: tuple(x,y)
        '''
        # pygame.display.update()
        x, y = pos
        if x >= self.rows or y >= self.cols or x < 0:
            self.draw()
            return 'out of bounds'
        # if  no  start
        # if self.cubes[x][y].colour != WHITE:
        #     return "no space to fill"
        if self.start == None and self.cubes[x][y].colour != endClr:
            self.start = self.cubes[x][y]
            self.cubes[x][y].clicked(6, startClr)
            # self.cubes[x][y].colour = startClr
            # self.cubes[x][y].placed = True
            # self.cubes[x][y].clickAnimation()

        # if no end
        elif self.end == None and self.cubes[x][y].colour != startClr:
            self.end = self.cubes[x][y]
            self.cubes[x][y].clicked(6, endClr)
            # self.cubes[x][y].colour = endClr
            # self.cubes[x][y].placed = True
            # self.cubes[x][y].clickAnimation()

        # end and start  are present
        elif self.cubes[x][y].colour not in [startClr, endClr]:
            self.cubes[x][y].clicked(6)
            # self.cubes[x][y].colour = obstacleClr
            # self.cubes[x][y].placed = True
            # self.cubes[x][y].clickAnimation()
        # self.draw()

    def a_star(self):
        '''A* algorithm to solve the grid'''
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
                        # updating the neighbour
                        neighbour.update_colour(CYAN, f_score[neighbour])

            # if this node is already visited update colour
            if current != self.start:
                current.update_colour(TURTLEGREEN)

        return False

    def reset(self):
        '''resets the board leaving start , end , walls '''
        for row in self.cubes:
            for cube in row:
                if cube.placed == False:
                    cube.reset()
                    cube.update()
        self.draw()

    def clear(self, noAnimation=False):
        '''clears the current board 
        :param noAnimation: False  
        '''
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
        '''reconstructs the path 
        :param came_from: dictionary containing its path from start to end
        '''
        current = self.end
        while current in came_from:
            current = came_from[current]
            current.update_colour(pathClr)
            current.clickAnimation(-6)

    def delete(self, x, y):
        '''delete a cube at  certain position'''
        if x >= self.rows or y >= self.cols or x < 0:
            self.draw()
            return -1
        self.cubes[x][y].reset()
        self.draw()
        if self.cubes[x][y] == self.start:
            self.start = None
        elif self.cubes[x][y] == self.end:
            self.end = None

    def toggle_theme(self, clr):
        global themeColour
        self.colour = clr
        themeColour = self.colour
        self.surface.fill(self.colour)
        self.animation()
        self.draw()


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows, WIN):
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

        # drawing canvas
        self.WIN = WIN

    def draw(self):
        '''draws the cube on to the screen'''
        win = self.WIN

        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap

        # this block of if-else draws a block on to screen
        if (not self.placed):
            # this {if} is for dark theme only , self.colour represents the theme
            if self.colouring and themeColour == BLACK:
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

    # drawing numbers
        if not self.value == None and self.show_numbers:
            text = PYtxt(str(self.value), int(rowGap*0.4), pygame.font.match_font(
                'consolas', bold=False, italic=False))
            win.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))

    def update(self):
        '''updates the  cube on the  screen'''
        self.draw()
        pygame.display.update()

    def get_pos(self):
        '''returns the row and coloumn in the grid'''
        return (self.row, self.col)

    def update_neighbours(self, grid):
        '''checks for neighbours and adds them here
        :param grid : A 2x2 matrix       
        '''
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
        '''returns if this cube is a barrier'''
        return self.colour == obstacleClr

    # used for animating in algoritm
    def update_colour(self, colour, value=None):
        '''updates  the color of the cube
        :param colour : colour to be updated
        :value : value of the cube its shown if show nums is on
        '''
        if not (self.colour == startClr or self.colour == endClr):
            self.colouring = True
            self.colour = colour
            # value is used for numbers
            if not value == None:
                self.value = value
        self.update()

    def reset(self):
        '''resets the cube  into original state'''
        self.placed = False
        self.colouring = False
        self.colour = WHITE
        self.value = None
        if themeColour == BLACK:
            rowGap = self.height / self.rows
            colGap = self.width / self.cols
            x = self.col * colGap
            y = self.row * rowGap
            pygame.draw.rect(self.WIN, BLACK,
                             pygame.Rect(x-1, y-1, colGap-1, rowGap-1))

    def clickAnimation(self, sub=0):
        '''animation for cube  when clicked
        :param subtract a value for speed calc
        '''
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        width = colGap - 10 - sub
        while True:
            width += 0.05
            pygame.draw.rect(self.WIN, self.colour,
                             pygame.Rect(x+(colGap-width)/2, y+(colGap-width)/2, width, width))
            pygame.display.update()
            if width >= colGap:
                break

        self.draw()

    def clicked(self, add=0, colour=None):
        '''clicks the cube useful for in maze generation'''
        if colour == None:
            self.colour = obstacleClr
        else:
            self.colour = colour

        self.placed = True
        self.clickAnimation(-6 + add)
