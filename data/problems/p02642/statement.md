# AtCoder Beginner Contest 170 - Not Divisible

- CodeNet ID: `p02642`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 400 points

## Problem Statement

Given is a number sequence A of length N.

Find the number of integers i \left(1 \leq i \leq N\right) with the following property:

- For every integer j \left(1 \leq j \leq N\right) such that i \neq j , A_j does not divide A_i.

## Constraints

- All values in input are integers.

- 1 \leq N \leq 2 \times 10^5

- 1 \leq A_i \leq 10^6

## Input

Input is given from Standard Input in the following format:
```text
N
A_1 A_2 \cdots A_N
```

## Output

Print the answer.

## Sample Input 1
```text
5
24 11 8 3 16
```

## Output for the Sample Input 1
```text
3
```

The integers with the property are 2, 3, and 4.

## Sample Input 2
```text
4
5 5 5 5
```

## Output for the Sample Input 2
```text
0
```

Note that there can be multiple equal numbers.

## Sample Input 3
```text
10
33 18 45 28 8 19 89 86 2 4
```

## Output for the Sample Input 3
```text
5
```
