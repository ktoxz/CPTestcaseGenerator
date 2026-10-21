# Electronic Fly

- CodeNet ID: `p00114`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

A computer scientist discovered a strange lifeform called an "electronic fly" inhabiting electronic space. While observing the behavior of the electronic fly, it was found that an electronic fly at point $(x, y, z)$ in this space moves to $(x', y', z')$ according to the following rules:

![Problem diagram 1](images/01.png)

Here, $a_1, m_1, a_2, m_2, a_3, m_3$ are positive integers determined for each individual electronic fly. $A mod B$ is the remainder when the positive integer $A$ is divided by the positive integer $B$.

Further observation revealed that some types of electronic flies, when placed at $(1, 1, 1)$, will always return to $(1, 1, 1)$ after some time. Such flies are named "returning flies"(1).

Write a program that takes the data of a returning fly as input and outputs the minimum number of moves ($>0$) to return to $(1, 1, 1)$. Note that $1 < a_1, m_1, a_2, m_2, a_3, m_3 < 2^{15}$.

(1) A fly returns when $a_1$ and $m_1$, $a_2$ and $m_2$, and $a_3$ and $m_3$ are each coprime (their greatest common divisor is 1).

## Input

Multiple datasets are given. Each dataset is given in the following format:

```text
a1 m1 a2 m2 a3 m3
```

The input ends with a line containing six 0s. The number of datasets does not exceed 50.

## Output

For each dataset, output the minimum number of moves (an integer) to return to $(1, 1, 1)$ on a single line.

## Sample Input 1

```text
2 5 3 7 6 13
517 1024 746 6561 4303 3125
0 0 0 0 0 0
```

## Output for the Sample Input 1

```text
12
116640000
```
