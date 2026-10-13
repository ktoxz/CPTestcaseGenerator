# B. Binary String Constructing

Source: https://codeforces.com/contest/1003/problem/B

B. Binary String Constructing
time limit per test
1 second
memory limit per test
256 megabytes
input
standard input
output
standard output

You are given three integers $$$a$$$, $$$b$$$ and $$$x$$$. Your task is to construct a binary string $$$s$$$ of length $$$n = a + b$$$ such that there are exactly $$$a$$$ zeroes, exactly $$$b$$$ ones and exactly $$$x$$$ indices $$$i$$$ (where $$$1 \le i  \lt  n$$$) such that $$$s_i \ne s_{i + 1}$$$. It is guaranteed that the answer always exists.
For example, for the string "01010" there are four indices $$$i$$$ such that $$$1 \le i  \lt  n$$$ and $$$s_i \ne s_{i + 1}$$$ ($$$i = 1, 2, 3, 4$$$). For the string "111001" there are two such indices $$$i$$$ ($$$i = 3, 5$$$).
Recall that binary string is a non-empty sequence of characters where each character is either 0 or 1.

Input
The first line of the input contains three integers $$$a$$$, $$$b$$$ and $$$x$$$ ($$$1 \le a, b \le 100, 1 \le x  \lt  a + b)$$$.

Output
Print only one string $$$s$$$, where $$$s$$$ is any binary string satisfying conditions described above. It is guaranteed that the answer always exists.

## Examples

## Sample Input 1
```text
2 2 1
```

## Output for the Sample Input 1
```text
1100
```

## Sample Input 2
```text
3 3 3
```

## Output for the Sample Input 2
```text
101100
```

## Sample Input 3
```text
5 3 6
```

## Output for the Sample Input 3
```text
01010100
```
