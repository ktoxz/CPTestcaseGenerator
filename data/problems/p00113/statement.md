# Repeating Decimals

- CodeNet ID: `p00113`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Given two positive integers $p$ and $q$, consider representing $p / q$ exactly as a decimal. (Assume $0 < p < q < 10^6$.)

In this case, the result will be one of the following:

- It can be represented exactly with a finite number of digits.
- It becomes a repeating decimal where a certain range of digits repeats.

If you determine the decimal part digit by digit using the same procedure as long division:

- If the division terminates (the remainder becomes 0), it was represented exactly up to that digit.
- If a remainder that has appeared once appears again, it has started to repeat.

Write a program that takes two integers $p$ and $q$ as input and outputs the decimal part of $p / q$. However:

- If the result can be represented exactly with a finite number of digits, output only the digits on one line.
- If the result is a repeating decimal, output it on two lines as follows:
  On the first line, output the digits up to and including the repeating part.
  On the second line, output spaces under the non-repeating part and "^" under the repeating part.

- In either case, it is guaranteed that the sequence of digits will not exceed 80 characters.

## Input

The input consists of multiple datasets. Each dataset consists of $p$ and $q$ given on one line, separated by a space. The number of datasets will not exceed 250.

## Output

For each dataset, if the decimal is non-repeating, output the decimal part (in this case, 1 line); if it is a repeating decimal, output the digits up to the repeating part and the symbol "^" indicating the repeating part (in this case, 2 lines).

## Sample Input 1

```text
1 12
10000 32768
1 11100
1 459550
```

## Output for the Sample Input 1

```text
083
  ^
30517578125
00009
  ^^^
00000217604178
  ^^^^^^^^^^^^
```
