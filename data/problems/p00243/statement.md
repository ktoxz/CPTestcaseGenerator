# Fill Game

- CodeNet ID: `p00243`
- Dataset: `AIZU`
- Time limit: `3000 ms`
- Memory limit: `131072 KB`

Tablet interface technology, which allows operation by touching the screen with a finger, has been applied to the field of games, and various types of games with new operational feels are being created. A game currently being developed by Company AZ is one such example.

The requirements for this software (game) are as follows:

- There is a 2D grid of X columns × Y rows on the screen.

- Each cell of the grid is painted in one of three colors: red (R), green (G), or brown (B).

- There are buttons R, G, and B to change the color of the cells. When one of these buttons is pressed, the top-leftmost cell (0,0) is changed to that color.

- When the color of the top-leftmost cell is changed, all adjacent cells painted in the same color as the original color of that cell are also changed to the specified color. In other words, all cells connected by the same original color are changed to the specified color.

In this game, the grid is filled in this manner, and the goal is to eventually make the entire grid a single color. A high score is given if the game is solved in fewer steps.

As a programmer at Company AZ, you have been tasked with developing a part of the logic for this game. First, to calculate the maximum score, you decided to create a program that determines the minimum number of button operations required to make the grid a single color when the game is solved in the shortest possible way.

![Problem diagram 1](images/01.png)

## Input

Multiple datasets are provided. The end of the input is indicated by two zeros. Each dataset is given in the following format:

```text
X Y
c1,1 c2,1 ... cX,1
c1,2 c2,2 ... cX,2
:
c1,Y c2,Y ... cX,Y
```

In the first line, the grid size X (columns) and Y (rows) (2 ≤ X, Y ≤ 10) are given. In the following Y lines, the characters $c_{i,j}$ representing the color of the cell at column $i$ and row $j$ are given, separated by spaces.

## Output

For each dataset, output the minimum number of button operations on a single line.

## Sample Input 1

```text
3 3
R G B
G G G
G B B
2 4
R G
G G
R B
B R
4 3
G G B R
G R R G
B G G R
0 0
```

## Output for the Sample Input 1

```text
2
4
4
```
