import pygame
# used for buttons
import pygame_gui
import time
# used for board creation
from grid import *
from colours import *
from store import *

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((720, 700))
pygame.display.set_caption('A* visualiser')
FPS = 20
manager = pygame_gui.UIManager(
    (WIN.get_width(), WIN.get_height()), 'themePygame_gui.json')


help = {}
showHelp = False
mouseClicks = True


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
        changeTheme()

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
    global help
    row_items = ((WIN.get_width()-board.width)-10)//60
    col_items = len(buttons)//row_items
    row_gap = (((WIN.get_width()-board.width)/row_items) - 60)/2
    col_gap = (((WIN.get_height())/col_items-40))
    start = board.width
    y = 10
    n = 1
    y_count = 0

    # creating buttons
    for name in buttons:
        globals()[name] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((start+n*row_gap, y + y_count*col_gap), (60, 40)), text=buttons[name]['text'],
                                                       manager=manager, tool_tip_text=None)
        # first index stores tool tip text , second index stores position of button
        help[buttons[name]['text']] = [buttons[name]
                                       ['tool_tip_text'], (start+n*row_gap, y + y_count*col_gap)]
        # updating so the bubttons will go next to each other
        start += 60
        n += 1
        # if the buttons fill the  whole width then they are pushed down
        if start+n*row_gap > WIN.get_width() - 60:
            start = board.width
            n = 1
            y_count += 1
            y += 40
    name = 'help_button'
    globals()[name] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, board.height+30), (30, 30)), text='?',
                                                   manager=manager, tool_tip_text=None)


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

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if mouseClicks:
                    checkButtonpress()

            # this is written here because we need to click even if mouse clicks is off
                if event.ui_element == help_button:
                    if showHelp == True:
                        board.draw()
                    showHelp = not showHelp
                    mouseClicks = not mouseClicks

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
