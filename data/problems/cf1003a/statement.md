# A. Polycarp's Pockets

Source: https://codeforces.com/contest/1003/problem/A

A. Polycarp's Pockets
time limit per test
1 second
memory limit per test
256 megabytes
input
standard input
output
standard output

Polycarp has $$$n$$$ coins, the value of the $$$i$$$-th coin is $$$a_i$$$. Polycarp wants to distribute all the coins between his pockets, but he cannot put two coins with the same value into the same pocket.
For example, if Polycarp has got six coins represented as an array $$$a = [1, 2, 4, 3, 3, 2]$$$, he can distribute the coins into two pockets as follows: $$$[1, 2, 3], [2, 3, 4]$$$.
Polycarp wants to distribute all the coins with the minimum number of used pockets. Help him to do that.

Input
The first line of the input contains one integer $$$n$$$ ($$$1 \le n \le 100$$$) — the number of coins.
The second line of the input contains $$$n$$$ integers $$$a_1, a_2, \dots, a_n$$$ ($$$1 \le a_i \le 100$$$) — values of coins.

Output
Print only one integer — the minimum number of pockets Polycarp needs to distribute all the coins so no two coins with the same value are put into the same pocket.

## Examples

## Sample Input 1
```text
6
1 2 4 3 3 2
```

## Output for the Sample Input 1
```text
2
```

## Sample Input 2
```text
1
100
```

## Output for the Sample Input 2
```text
1
```
