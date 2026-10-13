# B. Delete from the Left

Source: https://codeforces.com/contest/1005/problem/B

B. Delete from the Left
time limit per test
1 second
memory limit per test
256 megabytes
input
standard input
output
standard output

You are given two strings $$$s$$$ and $$$t$$$. In a single move, you can choose any of two strings and delete the first (that is, the leftmost) character. After a move, the length of the string decreases by $$$1$$$. You can't choose a string if it is empty.
For example:
by applying a move to the string "where", the result is the string "here",  by applying a move to the string "a", the result is an empty string "".
You are required to make two given strings equal using the fewest number of moves. It is possible that, in the end, both strings will be equal to the empty string, and so, are equal to each other. In this case, the answer is obviously the sum of the lengths of the initial strings.
Write a program that finds the minimum number of moves to make two given strings $$$s$$$ and $$$t$$$ equal.

Input
The first line of the input contains $$$s$$$. In the second line of the input contains $$$t$$$. Both strings consist only of lowercase Latin letters. The number of letters in each string is between 1 and $$$2\cdot10^5$$$, inclusive.

Output
Output the fewest number of moves required. It is possible that, in the end, both strings will be equal to the empty string, and so, are equal to each other. In this case, the answer is obviously the sum of the lengths of the given strings.

## Examples

## Sample Input 1
```text
test
west
```

## Output for the Sample Input 1
```text
2
```

## Sample Input 2
```text
codeforces
yes
```

## Output for the Sample Input 2
```text
9
```

## Sample Input 3
```text
test
yes
```

## Output for the Sample Input 3
```text
7
```

## Sample Input 4
```text
b
ab
```

## Output for the Sample Input 4
```text
1
```
