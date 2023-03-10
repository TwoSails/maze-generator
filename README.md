# Maze Generator

This is an application which generates a maze from base parameters using graphic tiles and the Wave Function Collapse Algorithm
![](mazes/default_scaled-complete.png)

## Testing

To complete the automated tests of this project.
Execute the command:
`python3 -m unittest discover tests`
in the root directory

## Running the algorithm
To run the program, ensure that all prerequisite libraries are installed.

This can be done by running the command:
`python3 -m pip install -r requirements.txt`

Run command: 
`python3 main.py`

The algorithm will then execute producing the output image as `default.png` inside the `mazeGenerator/mazes` directory. The input tiles can be viewed in `data/default`

## Virtual Environment
To enter the virtual environment, run:

* Unix or MacOS: `source venv/bin/activate`

* Windows: `venv/Scripts/activate.bat` (Windows virtual environment not tested)

## Cython Code
To compile the Cython code, run the command:

`python3 setup.py build_ext --inplace`