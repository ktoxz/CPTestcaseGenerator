# AtCoder Beginner Contest 174 - Logs

- CodeNet ID: `p02598`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 500 points

## Problem Statement

We have N logs of lengths A_1,A_2,\cdots A_N.

We can cut these logs at most K times in total. When a log of length L is cut at a point whose distance from an end of the log is t (0<t<L), it becomes two logs of lengths t and L-t.

Find the shortest possible length of the longest log after at most K cuts, and print it after rounding up to an integer.

## Constraints

- 1 \leq N \leq 2 \times 10^5

- 0 \leq K \leq 10^9

- 1 \leq A_i \leq 10^9

- All values in input are integers.

## Input

Input is given from Standard Input in the following format:
```text
N K
A_1 A_2 \cdots A_N
```

## Output

Print an integer representing the answer.

## Sample Input 1
```text
2 3
7 9
```

## Output for the Sample Input 1
```text
4
```

- First, we will cut the log of length 7 at a point whose distance from an end of the log is 3.5, resulting in two logs of length 3.5 each.

- Next, we will cut the log of length 9 at a point whose distance from an end of the log is 3, resulting in two logs of length 3 and 6.

- Lastly, we will cut the log of length 6 at a point whose distance from an end of the log is 3.3, resulting in two logs of length 3.3 and 2.7.

In this case, the longest length of a log will be 3.5, which is the shortest possible result. After rounding up to an integer, the output should be 4.

## Sample Input 2
```text
3 0
3 4 5
```

## Output for the Sample Input 2
```text
5
```

## Sample Input 3
```text
10 10
158260522 877914575 602436426 24979445 861648772 623690081 433933447 476190629 262703497 211047202
```

## Output for the Sample Input 3
```text
292638192
```
