# AtCoder Beginner Contest 174 - Repsept

- CodeNet ID: `p02596`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 300 points

## Problem Statement

Takahashi loves the number 7 and multiples of K.

Where is the first occurrence of a multiple of K in the sequence 7,77,777,\ldots? (Also see Output and Sample Input/Output below.)

If the sequence contains no multiples of K, print -1 instead.

## Constraints

- 1 \leq K \leq 10^6

- K is an integer.

## Input

Input is given from Standard Input in the following format:
```text
K
```

## Output

Print an integer representing the position of the first occurrence of a multiple of K. (For example, if the first occurrence is the fourth element of the sequence, print 4.)

## Sample Input 1
```text
101
```

## Output for the Sample Input 1
```text
4
```

None of 7, 77, and 777 is a multiple of 101, but 7777 is.

## Sample Input 2
```text
2
```

## Output for the Sample Input 2
```text
-1
```

All elements in the sequence are odd numbers; there are no multiples of 2.

## Sample Input 3
```text
999983
```

## Output for the Sample Input 3
```text
999982
```
