# A. Epic Game

Source: https://codeforces.com/contest/119/problem/A

A. Epic Game
time limit per test
2 seconds
memory limit per test
256 megabytes
input
standard input
output
standard output

Simon and Antisimon play a game. Initially each player receives one fixed positive integer that doesn't change throughout the game. Simon receives number a and Antisimon receives number b. They also have a heap of n stones. The players take turns to make a move and Simon starts. During a move a player should take from the heap the number of stones equal to the greatest common divisor of the fixed number he has received and the number of stones left in the heap. A player loses when he cannot take the required number of stones (i. e. the heap has strictly less stones left than one needs to take).
Your task is to determine by the given a, b and n who wins the game.

Input
The only string contains space-separated integers a, b and n (1 ≤ a, b, n ≤ 100) — the fixed numbers Simon and Antisimon have received correspondingly and the initial number of stones in the pile.

Output
If Simon wins, print "0" (without the quotes), otherwise print "1" (without the quotes).

## Examples

## Sample Input 1
```text
3 5 9
```

## Output for the Sample Input 1
```text
0
```

## Sample Input 2
```text
1 1 100
```

## Output for the Sample Input 2
```text
1
```
