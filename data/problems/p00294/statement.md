# Railway Line II

- CodeNet ID: `p00294`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

In the town where I live, there is a circular railway line consisting of $N$ stations, as shown in the figure. Each station on this line is assigned a number from $0$ to $N-1$ in order, and it costs 100 yen to travel to an adjacent station. Travel is possible in either direction.

![Problem diagram 1](images/01.png)

I want to go shopping at several stations on this line. Therefore, I decided to create a program to calculate the travel costs. Please create a program that finds the minimum cost (in yen) to visit all the shopping stations, starting from a specific station. You may visit the same station multiple times, and you may visit the stations in any order.

## Input

The input is given in the following format.

```text
N M p
d1
d2
:
dM
```

The first line contains the number of stations $N$ ($2 \le N \le 100000$), the number of stations to shop at $M$ ($1 \le M \le 10000$ and $M < N$), and the starting station number $p$ ($0 \le p \le N-1$). The following $M$ lines contain the station numbers $d_i$ ($0 \le d_i \le N-1$) where shopping will take place. Note that all $d_i$ are distinct, and $p$ is also distinct from all $d_i$.

## Output

Output the minimum cost on one line.

## Sample Input 1

```text
5 4 0
1
2
3
4
```

## Output for the Sample Input 1

```text
400
```

## Sample Input 2

```text
7 2 1
6
2
```

## Output for the Sample Input 2

```text
400
```
