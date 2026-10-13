# B. Sonya and Exhibition

Source: https://codeforces.com/contest/1004/problem/B

B. Sonya and Exhibition
time limit per test
1 second
memory limit per test
256 megabytes
input
standard input
output
standard output

Sonya decided to organize an exhibition of flowers. Since the girl likes only roses and lilies, she decided that only these two kinds of flowers should be in this exhibition.
There are $$$n$$$ flowers in a row in the exhibition. Sonya can put either a rose or a lily in the $$$i$$$-th position. Thus each of $$$n$$$ positions should contain exactly one flower: a rose or a lily.
She knows that exactly $$$m$$$ people will visit this exhibition. The $$$i$$$-th visitor will visit all flowers from $$$l_i$$$ to $$$r_i$$$ inclusive. The girl knows that each segment has its own beauty that is equal to the product of the number of roses and the number of lilies.
Sonya wants her exhibition to be liked by a lot of people. That is why she wants to put the flowers in such way that the sum of beauties of all segments would be maximum possible.

Input
The first line contains two integers $$$n$$$ and $$$m$$$ ($$$1\leq n, m\leq 10^3$$$) — the number of flowers and visitors respectively.
Each of the next $$$m$$$ lines contains two integers $$$l_i$$$ and $$$r_i$$$ ($$$1\leq l_i\leq r_i\leq n$$$), meaning that $$$i$$$-th visitor will visit all flowers from $$$l_i$$$ to $$$r_i$$$ inclusive.

Output
Print the string of $$$n$$$ characters. The $$$i$$$-th symbol should be «0» if you want to put a rose in the $$$i$$$-th position, otherwise «1» if you want to put a lily.
If there are multiple answers, print any.

## Examples

## Sample Input 1
```text
5 3
1 3
2 4
2 5
```

## Output for the Sample Input 1
```text
01100
```

## Sample Input 2
```text
6 3
5 6
1 4
4 6
```

## Output for the Sample Input 2
```text
110010
```
