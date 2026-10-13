# AtCoder Beginner Contest 167 - Colorful Blocks

- CodeNet ID: `p02685`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 500 points

## Problem Statement

There are N blocks arranged in a row. Let us paint these blocks.

We will consider two ways to paint the blocks different if and only if there is a block painted in different colors in those two ways.

Find the number of ways to paint the blocks under the following conditions:

- For each block, use one of the M colors, Color 1 through Color M, to paint it. It is not mandatory to use all the colors.

- There may be at most K pairs of adjacent blocks that are painted in the same color.

Since the count may be enormous, print it modulo 998244353.

## Constraints

- All values in input are integers.

- 1 \leq N, M \leq 2 \times 10^5

- 0 \leq K \leq N - 1

## Input

Input is given from Standard Input in the following format:
```text
N M K
```

## Output

Print the answer.

## Sample Input 1
```text
3 2 1
```

## Output for the Sample Input 1
```text
6
```

The following ways to paint the blocks satisfy the conditions: 112, 121, 122, 211, 212, and 221. Here, digits represent the colors of the blocks.

## Sample Input 2
```text
100 100 0
```

## Output for the Sample Input 2
```text
73074801
```

## Sample Input 3
```text
60522 114575 7559
```

## Output for the Sample Input 3
```text
479519525
```
