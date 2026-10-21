# Goldbach's Conjecture

- CodeNet ID: `p00056`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

It is known that every even number greater than or equal to 4 can be expressed as the sum of two prime numbers. This is called Goldbach's conjecture, and it has been verified by computer calculations to be true for very large numbers. For example, 10 can be expressed as the sum of two primes in 2 ways: 7 + 3 and 5 + 5.

Write a program that takes an integer $n$ as input and outputs the number of ways $n$ can be expressed as the sum of two prime numbers. Here, $n$ is between 4 and 50,000 inclusive. Note that the input $n$ is not necessarily an even number.

## Input

Multiple datasets are given. For each dataset, $n$ is given on one line. The input ends when $n$ is 0. The number of datasets does not exceed 10,000.

## Output

For each dataset, output the number of ways to express $n$ as the sum of two prime numbers on one line.

## Sample Input 1

```text
10
11
0
```

## Output for the Sample Input 1

```text
2
0
```
