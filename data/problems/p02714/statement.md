# AtCoder Beginner Contest 162 - RGB Triplets

- CodeNet ID: `p02714`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 400 points

## Problem Statement

We have a string S of length N consisting of R, G, and B.

Find the number of triples (i,~j,~k)~(1 \leq i < j < k \leq N) that satisfy both of the following conditions:

- S_i \neq S_j, S_i \neq S_k, and S_j \neq S_k.

- j - i \neq k - j.

## Constraints

- 1 \leq N \leq 4000

- S is a string of length N consisting of R, G, and B.

## Input

Input is given from Standard Input in the following format:
```text
N
S
```

## Output

Print the number of triplets in question.

## Sample Input 1
```text
4
RRGB
```

## Output for the Sample Input 1
```text
1
```

Only the triplet (1,~3,~4) satisfies both conditions. The triplet (2,~3,~4) satisfies the first condition but not the second, so it does not count.

## Sample Input 2
```text
39
RBRBGRBGGBBRRGBBRRRBGGBRBGBRBGBRBBBGBBB
```

## Output for the Sample Input 2
```text
1800
```
