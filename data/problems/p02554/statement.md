# AtCoder Beginner Contest 178 - Ubiquity

- CodeNet ID: `p02554`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 300 points

## Problem Statement

How many integer sequences A_1,A_2,\ldots,A_N of length N satisfy all of the following conditions?

- 0 \leq A_i \leq 9

- There exists some i such that A_i=0 holds.

- There exists some i such that A_i=9 holds.

The answer can be very large, so output it modulo 10^9 + 7.

## Constraints

- 1 \leq N \leq 10^6

- N is an integer.

## Input

Input is given from Standard Input in the following format:
```text
N
```

## Output

Print the answer modulo 10^9 + 7.

## Sample Input 1
```text
2
```

## Output for the Sample Input 1
```text
2
```

Two sequences \{0,9\} and \{9,0\} satisfy all conditions.

## Sample Input 2
```text
1
```

## Output for the Sample Input 2
```text
0
```

## Sample Input 3
```text
869121
```

## Output for the Sample Input 3
```text
2511445
```
