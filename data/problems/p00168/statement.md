# Kannon-do

- CodeNet ID: `p00168`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

There is a Kannon-do (Kannon temple) on the mountain behind Ichiro-kun's house. There are 30 steps from the foot of the mountain to this Kannon-do, and Ichiro-kun goes to visit it almost every day. Ichiro-kun can climb up to 3 steps at a time. While playing, he noticed that there are a very large number of ways to climb the stairs (the number of ways to skip steps).

Therefore, he thought he would try 10 different ways to climb per day and attempt every possible way. However, as someone well-versed in mathematics, you should know that Ichiro-kun's life would end before he could finish such a task.

To convince Ichiro-kun that his plan is impossible, please create a program that takes the number of steps $n$ as input and outputs the number of years it would take for Ichiro-kun to perform all possible ways of climbing, assuming he does 10 different ways per day. Calculate based on 365 days per year. If even a single day is required beyond a full year, it counts as another year. For example, 365 days is 1 year, and 366 days is 2 years.

## Input

A sequence of multiple datasets is given as input. The end of the input is indicated by a single line containing zero.
For each dataset, a single integer $n$ ($1 \le n \le 30$) representing the number of steps is given on one line.

The number of datasets does not exceed 30.

## Output

For each dataset, output the number of years (as an integer) required for Ichiro-kun to perform all possible ways of climbing on a single line.

## Sample Input 1

```text
1
10
20
25
0
```

## Output for the Sample Input 1

```text
1
1
34
701
```
