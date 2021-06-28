import pygame
# used for buttons
import pygame_gui
# used for board creation
from grid import *
from colours import *
from store import *

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((720, 600))
pygame.display.set_caption('A* visualiser')
FPS = 20
manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()), 'themePygame_gui.json')

# TODO: stop animations button , click  at other colours , intro


def checkButtonpress():
    global boardClr
    if event.ui_element == clear_button:
        board.clear()

    if event.ui_element == save_button:
        if board.start and board.end:
            save(board)

    if event.ui_element == load_button:
        load(board)

    if event.ui_element == run_button:
        if board.start and board.end:
            board.reset()
            board.a_star()

    if event.ui_element == toggleTheme_button:
        boardClr = toggleTheme(boardClr)
        Widgetsbackground.fill(boardClr)
        board.toggle_theme(boardClr)

    if event.ui_element == toggleNumber_button:
        board.show_numbers = not board.show_numbers
        board.draw()

    if event.ui_element == reset_button:
        board.reset()

    if event.ui_element == create_button:
        board._recursive_backtracking()


def checkKeypress():
    global boardClr
    if event.key == pygame.K_SPACE and board.start and board.end:
        board.reset()
        board.a_star()

    if event.key == pygame.K_c:
        board.clear()

    if event.key == pygame.K_s:
        if board.start and board.end:
            save(board)

    if event.key == pygame.K_l:
        load(board)

    if event.key == pygame.K_r:
        board.reset()

    if event.key == pygame.K_n:
        board.show_numbers = not board.show_numbers
        board.draw()

    if event.key == pygame.K_t:
        boardClr = toggleTheme(boardClr)
        Widgetsbackground.fill(boardClr)
        board.toggle_theme(boardClr)

    if event.key == pygame.K_m:
        board._recursive_backtracking()


def createbuttons():

    buttons = {
        'reset_button': {
            'text': 'Reset',
            "tool_tip_text": "Reset the board    ( r : key )",
        },

        'toggleNumber_button': {
            'text': 'Num',
            'tool_tip_text': "Toggle the show numbers ( n : key )"
        },

        'toggleTheme_button': {
            'text': 'Theme',
            'tool_tip_text': "Toggle the theme    ( t : key )"
        },

        'run_button': {
            'text': 'Start',
            'tool_tip_text': '"start the visualisation (space : key)"'
        },

        'clear_button': {
            'text': 'Clear',
            'tool_tip_text': 'clear the board or   (c : key)'
        },

        'save_button': {
            'text': 'Save',
            'tool_tip_text': 'saves the board or   (s : key)'
        },

        'load_button': {
            'text': 'Load',
            'tool_tip_text': 'loads the saved board or (l : key)'
        },
        'create_button': {
            'text': 'Create',
            'tool_tip_text': 'creates a random maze or (m : key)'
        }

    }

    row_items = ((WIN.get_width()-board.width)-10)//60
    col_items = len(buttons)//row_items
    row_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    col_gap = (((WIN.get_height())/col_items-40))
    start = board.width
    y = -10
    n = 1
    y_count = 1

    # creating buttons
    for name in buttons:
        globals()[name] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*row_gap, y + y_count*col_gap), (60, 40)), text=buttons[name]['text'],
                                                       manager=manager, tool_tip_text=buttons[name]['tool_tip_text'])
        # updating so the bubttons will go next to each other
        start += 60
        n += 1
        # if the buttons fill the  whole width then they are pushed down
        if start+n*row_gap > WIN.get_width() - 60:
            start = board.width
            n = 1
            y_count += 1
            y += 40


def toggleTheme(clr):
    if clr == WHITE:
        # return(BLACK, WHITE, (120, 120, 120))
        return BLACK
    else:
        # return(WHITE, absBlack, GREAY)
        return WHITE


board = Grid(30, 30, WIN.get_height(), WIN.get_height(), WIN)
board.animation()
board.draw()

Widgetsbackground = pygame.Surface(
    (WIN.get_width()-board.width, WIN.get_height()))
Widgetsbackground.fill(boardClr)


createbuttons()

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
            checkKeypress()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                checkButtonpress()

        manager.process_events(event)
    manager.update(time_delta)

    WIN.blit(Widgetsbackground, (board.width+3, 0))
    # this help_bar shows info of the board
    manager.draw_ui(WIN)
    pygame.display.update()


pygame.quit()
