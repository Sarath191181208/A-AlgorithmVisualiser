# saves the board and other things in json
import json
import os
from colours import *


def save(board):
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


def load(board):
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
