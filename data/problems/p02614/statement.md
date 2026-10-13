# AtCoder Beginner Contest 173 - H and V

- CodeNet ID: `p02614`
- Dataset: `AtCoder`
- Time limit: `1000 ms`
- Memory limit: `1048576 KB`

Score : 300 points

## Problem Statement

We have a grid of H rows and W columns of squares. The color of the square at the i-th row from the top and the j-th column from the left (1 \leq i \leq H, 1 \leq j \leq W) is given to you as a character c_{i,j}: the square is white if c_{i,j} is ., and black if c_{i,j} is #.

Consider doing the following operation:

- Choose some number of rows (possibly zero), and some number of columns (possibly zero). Then, paint red all squares in the chosen rows and all squares in the chosen columns.

You are given a positive integer K. How many choices of rows and columns result in exactly K black squares remaining after the operation? Here, we consider two choices different when there is a row or column chosen in only one of those choices.

## Constraints

- 1 \leq H, W \leq 6

- 1 \leq K \leq HW

- c_{i,j} is . or #.

## Input

Input is given from Standard Input in the following format:
```text
H W K
c_{1,1}c_{1,2}...c_{1,W}
c_{2,1}c_{2,2}...c_{2,W}
:
c_{H,1}c_{H,2}...c_{H,W}
```

## Output

Print an integer representing the number of choices of rows and columns satisfying the condition.

## Sample Input 1
```text
2 3 2
..#
###
```

## Output for the Sample Input 1
```text
5
```

Five choices below satisfy the condition.

- The 1-st row and 1-st column

- The 1-st row and 2-nd column

- The 1-st row and 3-rd column

- The 1-st and 2-nd column

- The 3-rd column

## Sample Input 2
```text
2 3 4
..#
###
```

## Output for the Sample Input 2
```text
1
```

One choice, which is choosing nothing, satisfies the condition.

## Sample Input 3
```text
2 2 3
##
##
```

## Output for the Sample Input 3
```text
0
```

## Sample Input 4
```text
6 6 8
..##..
.#..#.
#....#
######
#....#
#....#
```

## Output for the Sample Input 4
```text
208
```
