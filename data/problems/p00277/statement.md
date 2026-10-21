# Programming Contest

- CodeNet ID: `p00277`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

At Byakko University, a programming contest is held every year. Given that the total number of teams is $N$, each team is assigned a team ID from $1$ to $N$. The contest begins with all teams having a score of $0$ and lasts continuously for $L$ seconds.

This year's contest will be broadcast on television. During the contest, only the team with the highest score at that moment is shown on TV. However, if there are multiple teams with the same highest score, the team with the smallest team ID among them is shown. When the team to be shown changes, the camera switches instantaneously.

You have obtained the contest logs. The logs contain all records of when a team's score changed. Each record is given in the format: "Team $d$ earned $x$ points at $t$ seconds after the start of the contest." Note that points can be deducted, so the current score may become less than $0$.

Given the contest logs as input, create a program that reports the ID of the team that was shown on TV for the longest total duration from the start to the end of the contest.

## Input

The input consists of a single data set. The input is given in the following format:

```text
N R L
d1 t1 x1
d2 t2 x2
:
dR tR xR
```

The first line consists of three integers: $N$ ($2 \le N \le 100,000$), the number of teams; $R$ ($0 \le R \le 1,000,000$), the number of records in the log; and $L$ ($1 \le L \le 1,000,000$), the duration (length) of the contest. The following $R$ lines provide the information for each record. Each record indicates that team $d_i$ ($1 \le d_i \le N$) earned or lost $x_i$ ($-1000 \le x_i \le 1000$) points at $t_i$ ($0 < t_i < L$) seconds after the start of the contest. Here, $t_i$ and $x_i$ are integers, and $t_{i-1} \le t_i$.

## Output

Output the ID of the team that was shown on TV for the longest total duration from the start to the end of the contest on a single line. If there are multiple teams with the same longest duration, output the one with the smallest team ID.

## Sample Input 1

```text
3 4 600
3 100 5
1 200 10
2 400 20
3 500 20
```

## Output for the Sample Input 1

```text
1
```

## Sample Input 2

```text
3 5 600
3 100 5
1 200 10
2 300 30
1 400 -8
2 400 -27
```

## Output for the Sample Input 2

```text
3
```
