# The Giant Tree Carver

- CodeNet ID: `p00283`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

You are trying to cut down a giant tree in front of you using $N$ types of tools. Initially, the tree's durability is $D$ and your experience points are $0$. When you strike the tree once with tool $i$, the tree's durability decreases by $a_i$ and you gain $e_i$ experience points. However, to use tool $i$, you must have experience points of $r_i$ or more. The tree falls when its durability becomes $0$ or less.

Given the information about the tree's durability and the tools, write a program to find the minimum number of times you must strike the tree to cut it down.

## Input

The input consists of multiple datasets. The end of the input is indicated by two lines of zeros. Each dataset is given in the following format:

```text
D N
a1 e1 r1
a2 e2 r2
:
aN eN rN
```

The first line contains an integer $D$ ($1 \le D \le 100$) representing the tree's durability and an integer $N$ ($1 \le N \le 100$) representing the number of types of tools. The following $N$ lines contain information for tools $1$ to $N$. $a_i$ ($0 \le a_i \le 100$) and $e_i$ ($0 \le e_i \le 100$) represent the amount by which the tree's durability decreases and the experience points you gain, respectively, by using tool $i$ once. $r_i$ ($0 \le r_i \le 100$) represents the experience points required to use the tool. $a_i, e_i, r_i$ are all integers.

The number of datasets does not exceed 50.

## Output

Output the minimum number of times the tree must be struck to cut it down on a single line. However, if it is impossible to cut down the tree, output NA.

## Sample Input 1

```text
15 4
1 1 0
1 2 2
5 10 5
8 1 15
60 4
5 2 0
8 8 2
3 5 0
49 0 18
100 1
1 1 1
0 0
```

## Output for the Sample Input 1

```text
6
4
NA
```
