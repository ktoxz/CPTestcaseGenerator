# Factorial II

- CodeNet ID: `p00052`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

n! = n × (n − 1) × (n − 2) × ... × 3 × 2 × 1

is called the factorial of n. For example, the factorial of 12 is

12! = 12 × 11 × 10 × 9 × 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1 = 479001600

which has 2 consecutive zeros at the end.

Write a program that takes an integer n as input and outputs the number of consecutive zeros at the end of n!. Assume that n is a positive integer less than or equal to 20000.

## Input

Multiple sets of data are given. For each set, n (n ≤ 20000) is given on one line. The input ends when n is 0.

The number of data sets does not exceed 20.

## Output

For each set of data, output the number of consecutive zeros at the end of n! on one line.

## Sample Input 1

```text
2
12
10000
0
```

## Output for the Sample Input 1

```text
0
2
2499
```
