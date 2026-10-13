# A. Stages

Source: https://codeforces.com/contest/1011/problem/A

A. Stages
time limit per test
1 second
memory limit per test
256 megabytes
input
standard input
output
standard output

Natasha is going to fly to Mars. She needs to build a rocket, which consists of several stages in some order. Each of the stages is defined by a lowercase Latin letter. This way, the rocket can be described by the string — concatenation of letters, which correspond to the stages.
There are $$$n$$$ stages available. The rocket must contain exactly $$$k$$$ of them. Stages in the rocket should be ordered by their weight. So, after the stage with some letter can go only stage with a letter, which is at least two positions after in the alphabet (skipping one letter in between, or even more). For example, after letter 'c' can't go letters 'a', 'b', 'c' and 'd', but can go letters 'e', 'f', ..., 'z'.
For the rocket to fly as far as possible, its weight should be minimal. The weight of the rocket is equal to the sum of the weights of its stages. The weight of the stage is the number of its letter in the alphabet. For example, the stage 'a 'weighs one ton,' b 'weighs two tons, and' z' — $$$26$$$ tons.
Build the rocket with the minimal weight or determine, that it is impossible to build a rocket at all. Each stage can be used at most once.

Input
The first line of input contains two integers — $$$n$$$ and $$$k$$$ ($$$1 \le k \le n \le 50$$$) – the number of available stages and the number of stages to use in the rocket.
The second line contains string $$$s$$$, which consists of exactly $$$n$$$ lowercase Latin letters. Each letter defines a new stage, which can be used to build the rocket. Each stage can be used at most once.

Output
Print a single integer — the minimal total weight of the rocket or -1, if it is impossible to build the rocket at all.

## Examples

## Sample Input 1
```text
5 3
xyabd
```

## Output for the Sample Input 1
```text
29
```

## Sample Input 2
```text
7 4
problem
```

## Output for the Sample Input 2
```text
34
```

## Sample Input 3
```text
2 2
ab
```

## Output for the Sample Input 3
```text
-1
```

## Sample Input 4
```text
12 1
abaabbaaabbb
```

## Output for the Sample Input 4
```text
1
```
