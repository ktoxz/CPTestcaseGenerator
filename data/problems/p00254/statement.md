# All Numbers Lead to 6174

- CodeNet ID: `p00254`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

For a four-digit number $N$ consisting of digits from 0 to 9, perform the following operation:

- Let $L$ be the number obtained by arranging the digits of $N$ in descending order.

- Let $S$ be the number obtained by arranging the digits of $N$ in ascending order.

- Let the difference $L-S$ be the new $N$ (this completes one operation).

- Repeat from step 1 for the new $N$.

It is known that, except for cases where all digits are the same (e.g., 0000, 1111), any four-digit number will eventually become 6174. For example, if $N = 2012$:

1st time ($N = 2012$): $L = 2210, S = 0122, L-S = 2088$
2nd time ($N = 2088$): $L = 8820, S = 0288, L-S = 8532$
3rd time ($N = 8532$): $L = 8532, S = 2358, L-S = 6174$

Thus, it reaches 6174 in 3 operations.

Given a four-digit number consisting of digits from 0 to 9, please create a program that calculates how many operations are required to reach 6174.

## Input

The input consists of multiple datasets. The end of the input is indicated by a single line containing 0000. Each dataset is given in the following format:

```text
N
```

A dataset consists of one line, where $N$ ($1 \le N \le 9999$) represents a four-digit number. If $N < 1000$, the upper digits are padded with 0.

The number of datasets does not exceed 10000.

## Output

For each dataset, output the number of operations required to reach 6174 on a single line. However, if a number where all digits are the same is given as input, output NA.

## Sample Input 1

```text
6174
2012
3333
0000
```

## Output for the Sample Input 1

```text
0
3
NA
```
