# A. Reorder the Array

Source: https://codeforces.com/contest/1007/problem/A

A. Reorder the Array
time limit per test
2 seconds
memory limit per test
256 megabytes
input
standard input
output
standard output

You are given an array of integers. Vasya can permute (change order) its integers. He wants to do it so that as many as possible integers will become on a place where a smaller integer used to stand. Help Vasya find the maximal number of such integers.
For instance, if we are given an array $$$[10, 20, 30, 40]$$$, we can permute it so that it becomes $$$[20, 40, 10, 30]$$$. Then on the first and the second positions the integers became larger ($$$20 \gt 10$$$, $$$40 \gt 20$$$) and did not on the third and the fourth, so for this permutation, the number that Vasya wants to maximize equals $$$2$$$. Read the note for the first example, there is one more demonstrative test case.
Help Vasya to permute integers in such way that the number of positions in a new array, where integers are greater than in the original one, is maximal.

Input
The first line contains a single integer $$$n$$$ ($$$1 \leq n \leq 10^5$$$) — the length of the array.
The second line contains $$$n$$$ integers $$$a_1, a_2, \ldots, a_n$$$ ($$$1 \leq a_i \leq 10^9$$$) — the elements of the array.

Output
Print a single integer — the maximal number of the array's elements which after a permutation will stand on the position where a smaller element stood in the initial array.

## Examples

## Sample Input 1
```text
7
10 1 1 1 5 5 3
```

## Output for the Sample Input 1
```text
4
```

## Sample Input 2
```text
5
1 1 1 1 1
```

## Output for the Sample Input 2
```text
0
```
