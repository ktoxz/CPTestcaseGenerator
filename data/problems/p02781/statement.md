# AtCoder Beginner Contest 154 - Almost Everywhere Zero

- CodeNet ID: `p02781`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 500 points

## Problem Statement

Find the number of integers between 1 and N (inclusive) that contains exactly K non-zero digits when written in base ten.

## Constraints

- 1 \leq N < 10^{100}

- 1 \leq K \leq 3

## Input

Input is given from Standard Input in the following format:
```text
N
K
```

## Output

Print the count.

## Sample Input 1
```text
100
1
```

## Output for the Sample Input 1
```text
19
```

The following 19 integers satisfy the condition:

- 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100

## Sample Input 2
```text
25
2
```

## Output for the Sample Input 2
```text
14
```

The following 14 integers satisfy the condition:

- 11,12,13,14,15,16,17,18,19,21,22,23,24,25

## Sample Input 3
```text
314159
2
```

## Output for the Sample Input 3
```text
937
```

## Sample Input 4
```text
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
3
```

## Output for the Sample Input 4
```text
117879300
```
