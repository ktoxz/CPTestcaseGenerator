# A. Homework

Source: https://codeforces.com/contest/101/problem/A

A. Homework
time limit per test
2 seconds
memory limit per test
256 megabytes
input
standard input
output
standard output

Once when Gerald studied in the first year at school, his teacher gave the class the following homework. She offered the students a string consisting of n small Latin letters; the task was to learn the way the letters that the string contains are written. However, as Gerald is too lazy, he has no desire whatsoever to learn those letters. That's why he decided to lose some part of the string (not necessarily a connected part). The lost part can consist of any number of segments of any length, at any distance from each other. However, Gerald knows that if he loses more than k characters, it will be very suspicious.
Find the least number of distinct characters that can remain in the string after no more than k characters are deleted. You also have to find any possible way to delete the characters.

Input
The first input data line contains a string whose length is equal to n (1 ≤ n ≤ 105). The string consists of lowercase Latin letters. The second line contains the number k (0 ≤ k ≤ 105).

Output
Print on the first line the only number m — the least possible number of different characters that could remain in the given string after it loses no more than k characters.
Print on the second line the string that Gerald can get after some characters are lost. The string should have exactly m distinct characters. The final string should be the subsequence of the initial string. If Gerald can get several different strings with exactly m distinct characters, print any of them.

## Examples

## Sample Input 1
```text
aaaaa
4
```

## Output for the Sample Input 1
```text
1
aaaaa
```

## Sample Input 2
```text
abacaba
4
```

## Output for the Sample Input 2
```text
1
aaaa
```

## Sample Input 3
```text
abcdefgh
10
```

## Output for the Sample Input 3
```text
0
```
