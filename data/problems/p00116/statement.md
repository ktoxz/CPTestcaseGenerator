# Rectangle Search

- CodeNet ID: `p00116`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

There is a grid of cells consisting of $H$ rows and $W$ columns, for a total of $W \times H$ cells. Some of the cells are marked. Read the state of the marks for each cell and create a program that outputs the area of the largest rectangle consisting only of unmarked cells.

The input data consists of $H$ lines, each containing $W$ characters. For example, the following data is given:

```text
..*....**.
..........
**....***.
....*.....
..*.......
...**.....
.*.*......
..........
..**......
.*..*.....
```

Each line of the input data represents one row of cells. In the input strings, `.` (period) indicates an unmarked cell, and `*` (asterisk) indicates a marked cell. The input strings contain no characters other than periods, asterisks, and line breaks.

In the example above, the rectangle indicated by 0 in the figure below is the largest.

```text
..*....**.
..........
**....***.
....*00000
..*..00000
...**00000
.*.*.00000
.....00000
..**.00000
.*..*00000
```

Therefore, the correct answer is to output 35. If all cells are marked, output 0.

## Input

Multiple datasets are given. Each dataset begins with a line consisting of $H$ and $W$ separated by a space, followed by a rectangle of $H \times W$. Both $H$ and $W$ are 500 or less.

The input ends with a line containing two 0s. The number of datasets does not exceed 20.

## Output

For each dataset, output the area of the largest rectangle on a single line.

## Sample Input 1

```text
10 10
...*....**
..........
**....**..
........*.
..*.......
**........
.*........
..........
....*..***
.*....*...
10 10
..*....*..
.*.*...*..
*****..*..
*...*..*..
*...*..*..
..........
****.*...*
..*..*...*
.*...*...*
****..***.
2 3
...
...
0 0
```

## Output for the Sample Input 1

```text
28
12
6
```
