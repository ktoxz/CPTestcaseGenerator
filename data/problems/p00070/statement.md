# Combination of Number Sequences

- CodeNet ID: `p00070`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Consider a sequence of $n$ numbers $k_1, k_2, \dots, k_n$ using integers from 0 to 9. Read a positive integer $n$ and an integer $s$, and create a program that outputs the number of sequences of $n$ numbers such that

$k_1 + 2 \times k_2 + 3 \times k_3 + \dots + n \times k_n = s$

However, in a single "sequence of $n$ numbers," the same number must not appear two or more times.

## Input

The input consists of multiple datasets. For each dataset, $n$ ($1 \le n \le 10$) and $s$ ($0 \le s \le 10,000$) are given on one line, separated by a space.

The number of datasets does not exceed 100.

## Output

For each dataset, output the number of combinations of $n$ integers whose sum is $s$ on a single line.

## Sample Input 1

```text
3 10
3 1
```

## Output for the Sample Input 1

```text
8
0
```
