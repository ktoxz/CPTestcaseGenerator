# AtCoder Beginner Contest 130 - Common Subsequence

- CodeNet ID: `p03003`
- Dataset: `AtCoder`
- Time limit: `2000 ms`
- Memory limit: `1048576 KB`

Score : 500 points

## Problem Statement

You are given two integer sequences S and T of length N and M, respectively, both consisting of integers between 1 and 10^5 (inclusive).

In how many pairs of a subsequence of S and a subsequence of T do the two subsequences are the same in content?

Here the subsequence of A is a sequence obtained by removing zero or more elements from A and concatenating the remaining elements without changing the order.

For both S and T, we distinguish two subsequences if the sets of the indices of the removed elements are different, even if the subsequences are the same in content.

Since the answer can be tremendous, print the number modulo 10^9+7.

## Constraints

- 1 \leq N, M \leq 2 \times 10^3

- The length of S is N.

- The length of T is M.

- 1 \leq S_i, T_i \leq 10^5

- All values in input are integers.

## Input

Input is given from Standard Input in the following format:
```text
N M
S_1 S_2 ... S_{N-1} S_{N}
T_1 T_2 ... T_{M-1} T_{M}
```

## Output

Print the number of pairs of a subsequence of S and a subsequence of T such that the subsequences are the same in content, modulo 10^9+7.

## Sample Input 1
```text
2 2
1 3
3 1
```

## Output for the Sample Input 1
```text
3
```

S has four subsequences: (), (1), (3), (1, 3).

T has four subsequences: (), (3), (1), (3, 1).

There are 1 \times 1 pair of subsequences in which the subsequences are both (), 1 \times 1 pair of subsequences in which the subsequences are both (1), and 1 \times 1 pair of subsequences in which the subsequences are both (3), for a total of three pairs.

## Sample Input 2
```text
2 2
1 1
1 1
```

## Output for the Sample Input 2
```text
6
```

S has four subsequences: (), (1), (1), (1, 1).

T has four subsequences: (), (1), (1), (1, 1).

There are 1 \times 1 pair of subsequences in which the subsequences are both (), 2 \times 2 pairs of subsequences in which the subsequences are both (1), and 1 \times 1 pair of subsequences in which the subsequences are both (1,1), for a total of six pairs. Note again that we distinguish two subsequences if the sets of the indices of the removed elements are different, even if the subsequences are the same in content.

## Sample Input 3
```text
4 4
3 4 5 6
3 4 5 6
```

## Output for the Sample Input 3
```text
16
```

## Sample Input 4
```text
10 9
9 6 5 7 5 9 8 5 6 7
8 6 8 5 5 7 9 9 7
```

## Output for the Sample Input 4
```text
191
```

## Sample Input 5
```text
20 20
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

## Output for the Sample Input 5
```text
846527861
```

Be sure to print the number modulo 10^9+7.
