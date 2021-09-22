from typing import Dict, Union
import pygame
# used for buttons
import pygame_gui
import time

# required for altering with button class 
from pygame_gui.core.interfaces.container_interface import IContainerLikeInterface
from pygame_gui.core.interfaces.manager_interface import IUIManagerInterface
from pygame_gui.core.ui_element import ObjectID, UIElement
# used for board creation
from grid import *
from colours import *

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((720, 700))
pygame.display.set_caption('A* visualiser')
FPS = 60
manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()), 'themePygame_gui.json')


help = {}
showHelp = False
mouseClicks = True

class Btn(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect: pygame.Rect, text: str, manager: IUIManagerInterface, container: Union[IContainerLikeInterface, None] = None, tool_tip_text: Union[str, None] = None, starting_height: int = 1, parent_element: UIElement = None, object_id: Union[ObjectID, str, None] = None, anchors: Dict[str, str] = None, allow_double_clicks: bool = False, visible: int = 1,func = None):
        self.func = func
        super().__init__(relative_rect, text, manager, container=container, tool_tip_text=tool_tip_text, starting_height=starting_height, parent_element=parent_element, object_id=object_id, anchors=anchors, allow_double_clicks=allow_double_clicks, visible=visible)
    
    def update(self, time_delta: float):
        if self.check_pressed() and self.func is not None:
            self.func()
        return super().update(time_delta)

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def changeTheme():
    global boardClr
    boardClr = toggleTheme(boardClr)
    textBackground.fill(boardClr)
    WIN.blit(textBackground, (1, board.height+1))
    Widgetsbackground.fill(boardClr)
    WIN.blit(Widgetsbackground, (board.width+1, 0))
    pygame.display.update()
    board.toggle_theme(boardClr)


def checkKeypress():
    global boardClr
    if event.key == pygame.K_SPACE and board.start and board.end:
        board.reset()
        board.a_star()

    if event.key == pygame.K_c:
        board.clear()

    if event.key == pygame.K_s:
        if board.start and board.end:
            board.save()

    if event.key == pygame.K_l:
        board.load()

    if event.key == pygame.K_r:
        board.reset()

    if event.key == pygame.K_n:
        board.show_numbers = not board.show_numbers
        board.draw()

    if event.key == pygame.K_t:
        changeTheme()

    if event.key == pygame.K_m:
        board._recursive_backtracking()


def showtext():
    text = PYtxt("  . Left click to insert      .Right click to delete", 18)
    txtHeight = text.get_height()*1.8
    WIN.blit(text, (80, board.height+txtHeight))
    if board.show_numbers:

        text = PYtxt("N", 16, fontColour=helperTxtClr)
        x = board.width - text.get_width()
        y = board.height + txtHeight
        WIN.blit(text, (x, y))
        pygame.draw.rect(WIN, textClr,
                         pygame.Rect(x-5, y-4, text.get_width()+10, text.get_height()+6), 1)

def toggle_help():
    global showHelp, mouseClicks
    if showHelp == True:
            board.draw()
    showHelp = not showHelp
    mouseClicks = not mouseClicks

def createbuttons():

    global help
    row_items = ((WIN.get_width()-board.width)-10)//60
    col_items = 9//row_items
    row_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    col_gap = (((WIN.get_height())/col_items-40))
    start = board.width
    y = 10
    n = 1
    y_count = 0

    # creating buttons
    for (btn_name,tool_tip,func) in [
        ("Reset","Reset the board    ( r : key )",lambda:board.reset()),
        ("NUM", "Toggle the show numbers ( n : key )",lambda: board.toggle_show_numbers()),
        ("Theme", "Toggle the theme    ( t : key )",lambda: board.toggle_theme()),
        ("Start", "start the visualisation (space : key)",lambda: board.toggle_theme()),
        ("Start", "start the visualisation (space : key)",lambda: board.start()),
        ("Clear", "clear the board or   (c : key)",lambda: board.clear()),
        ("Save", "saves the board or   (s : key)",lambda: board.save()),
        ("Load", "loads the saved board or (l : key)",lambda: board.load()),
        ("Create", "creates a random maze or (m : key)",lambda: board.generate_maze()),
    ]:
        Btn(relative_rect=pygame.Rect((start+n*row_gap, y + y_count*col_gap), (60, 40)), text= btn_name,
                                manager=manager, tool_tip_text=None,
                                func= func)
        
        # first index stores tool tip text , second index stores position of button
        help[btn_name] = tool_tip, (start+n*row_gap, y + y_count*col_gap)
        # updating so the buttons will go next to each other
        start += 20
        n += 1
        # if the buttons fill the  whole width then they are pushed down
        if start+n*row_gap > WIN.get_width() - 60:
            start = board.width
            n = 1
            y_count += 1
            y += 20
    Btn(relative_rect=pygame.Rect((10, board.height+30), (30, 30)), text='?',
manager=manager, tool_tip_text=None, func = lambda : toggle_help() )


def toggleTheme(clr):
    if clr == WHITE:
        # return(BLACK, WHITE, (120, 120, 120))
        return BLACK
    else:
        # return(WHITE, absBlack, GREAY)
        return WHITE


WIN.fill(WHITE)


board = Grid(30, 30, 600, 600, WIN)
board.animation()
board.draw()

Widgetsbackground = pygame.Surface(
    (WIN.get_width()-board.width, WIN.get_height()))
textBackground = pygame.Surface(
    (WIN.get_width()-Widgetsbackground.get_width(), WIN.get_height()-board.height))
textBackground.fill(boardClr)
Widgetsbackground.fill(boardClr)
pygame.display.update()

# this reqires the dimensions of the board so its placed after creating board
createbuttons()

run = True

while run:

    clock.tick(FPS)
    time_delta = clock.tick(FPS)/1000.0

    # checks for left click
    if pygame.mouse.get_pressed()[0] and mouseClicks:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.clicked((y, x))

    # checks for right click
    elif pygame.mouse.get_pressed()[2] and mouseClicks:
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        board.delete(y, x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if mouseClicks:
                checkKeypress()

        manager.process_events(event)
    manager.update(time_delta)
    WIN.blit(textBackground, (1, board.height+1))
    WIN.blit(Widgetsbackground, (board.width+1, 0))

    showtext()
    if showHelp:
        WIN.fill(boardClr)
        for key in help:
            txt = help[key][0]
            txt += '   '
            pos_x, pos_y = help[key][1]
            text = PYtxt(txt, 18)
            WIN.blit(text, (pos_x-text.get_width(),
                     pos_y+(text.get_height()/2)))

    manager.draw_ui(WIN)

    pygame.display.update()


pygame.quit()
