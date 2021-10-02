# A\* Visualiser

A simple application in **python** using **pygame** inspired from tech with tim (a youtuber) visualses A\* algorithm.

# Description

A grid layout is followed in the application. Left click to insert blocks, Right to delete. This application visualises what is the shortest path between the points is.

## Demo

![Image](https://github.com/Sarath191181208/A-AlgorithmVisualiser/blob/master/images/Screenshot.png)

## Features

- A **Reset button** to clear the board without removing start and end.
- A **Theme button** to change the theme on board.
- A **Clear button** to totally clear the board.
- A **Start button** to start the visualization.
- Save/Load.
- A **Create button** which uses recursive backtracking to create a pseudo random board.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/A-AlgorithmVisualiser
```

Go to the project directory

```bash
  cd ./A-AlgorithmVisualiser
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## References

Tech With Tim : https://github.com/techwithtim/A-Path-Finding-Visualization
Tech With Tim : https://www.youtube.com/watch?v=JtiK0DOeI4A

## Usage

- **Right click to delete the block.**
- Left click to insert.
- All the buttons are explained in features section.

## Hot keys

- SPACE : Start visualization
- C : Clear
- S : Save
- O : Load
- R : Reset
- N : Shows scores of the blocks **( ! extremely slow)**.
- T : Toggle theme.
- M : Create maze.

## Requirements

- python `Make sure to add to path`
- pygame `pip install pygame`
- pygame_gui `pip install pygame_gui`
