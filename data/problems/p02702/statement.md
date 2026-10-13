# AtCoder Beginner Contest 164 - Multiple of 2019

- CodeNet ID: `p02702`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 400 points

## Problem Statement

Given is a string S consisting of digits from 1 through 9.

Find the number of pairs of integers (i,j) (1 ≤ i ≤ j ≤ |S|) that satisfy the following condition:

Condition: In base ten, the i-th through j-th characters of S form an integer that is a multiple of 2019.

## Constraints

- 1 ≤ |S| ≤ 200000

- S is a string consisting of digits from 1 through 9.

## Input

Input is given from Standard Input in the following format:
```text
S
```

## Output

Print the number of pairs of integers (i,j) (1 ≤ i ≤ j ≤ |S|) that satisfy the condition.

## Sample Input 1
```text
1817181712114
```

## Output for the Sample Input 1
```text
3
```

Three pairs - (1,5), (5,9), and (9,13) - satisfy the condition.

## Sample Input 2
```text
14282668646
```

## Output for the Sample Input 2
```text
2
```

## Sample Input 3
```text
2119
```

## Output for the Sample Input 3
```text
0
```

No pairs satisfy the condition.
