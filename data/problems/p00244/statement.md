# Hot Spring Trip

- CodeNet ID: `p00244`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Takeshi, who loves hot springs, is planning a trip to a certain hot spring resort during his next long vacation. He intends to travel by transferring between long-distance buses and wants to reach his destination while spending as little money as possible. Although he has some savings, Takeshi is uncertain about his funds, so he decided to consult his grandfather. Impressed by the plan, his grandfather gave Takeshi a special ticket.

This ticket allows him to travel two consecutive sections of long-distance buses for free, exactly once. Depending on how it is used, it can significantly reduce travel costs, but to maximize its effect, he needs to devise a solid plan.

There are a total of $n$ points, including the departure point, the destination, and transit points, and $m$ routes connecting two points. Each point is assigned a number from 1 to $n$. The departure point is 1, and the destination is $n$. Route information is represented by the two points $a$ and $b$ that the route connects, and the fare $c$. Due to the effect of the special ticket, he can pass through two consecutive routes from any point for a fare of 0 exactly once. However, even if he passes through the destination midway, it does not count as having reached the destination.

Create a program that takes the total number of departure, destination, and transit points $n$, the number of routes $m$, and the information for each route as input, and outputs the minimum fare. It is guaranteed that a path from the departure point to the destination always exists.

## Input

Multiple data sets are given. The end of the input is indicated by two lines of zeros. Each data set is given in the following format:

```text
n m
a1 b1 c1
a2 b2 c2
:
am bm cm
```

The first line contains the total number of departure, destination, and transit points $n$ ($2 \le n \le 100$) and the number of routes $m$ ($1 \le m \le 300$). The following $m$ lines contain the information for each route $a_i, b_i, c_i$ ($1 \le c_i \le 1000$).

The number of data sets does not exceed 40.

## Output

For each input data set, output the minimum fare on one line.

## Sample Input 1

```text
2 1
1 2 5
3 2
1 2 5
2 3 5
6 9
1 2 7
1 3 9
1 5 14
2 3 10
2 4 15
3 4 11
3 5 2
4 5 9
4 6 8
0 0
```

## Output for the Sample Input 1

```text
5
0
7
```
