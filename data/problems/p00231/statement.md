# Dangerous Bridge

- CodeNet ID: `p00231`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

In Aizu Komatsu Village, located far north of Aizu Wakamatsu City, a bridge called "Yabashi" is the only means of traveling to surrounding villages. Despite the high volume of pedestrians, the bridge has deteriorated to the point where it looks as if it could collapse at any moment.

![Problem diagram 1](images/01.png)

Yabashi has a strength that can withstand up to 150 [kg]. For example, a person weighing 80 [kg] and a person weighing 50 [kg] can cross at the same time, but if a person weighing 90 [kg] starts crossing while a person weighing 80 [kg] is already crossing, Yabashi will collapse.

If Yabashi collapses, the people of Aizu Komatsu Village will lose their means of traveling to surrounding villages. Therefore, as the only programmer in the village, you have decided to create a program to determine whether the bridge will collapse or not based on how the pedestrians cross the bridge, in order to protect the lives of the villagers.

Given the number of pedestrians crossing the bridge $n$ ($1 \le n \le 100$), the weight of each pedestrian $m_i$ ($1 \le m_i \le 100$), the time they start crossing the bridge $a_i$, and the time they finish crossing the bridge $b_i$ ($0 \le a_i, b_i < 2^{31}$), create a program that outputs "OK" if the bridge does not collapse and "NG" if it does. Note that Yabashi collapses if the sum of the weights of the pedestrians on the bridge exceeds 150 [kg]. Additionally, a pedestrian is on the bridge at time $a_i$, but is no longer on the bridge at time $b_i$.

## Input

A sequence of multiple datasets is given as input. The end of the input is indicated by a single line containing zero. Each dataset is given in the following format:

```text
n
m1 a1 b1
m2 a2 b2
:
mn an bn
```

The number of datasets does not exceed 1200.

## Output

For each input dataset, output whether the bridge collapses or not on a single line.

## Sample Input 1

```text
3
80 0 30
50 5 25
90 27 50
3
80 0 30
70 5 25
71 30 50
0
```

## Output for the Sample Input 1

```text
NG
OK
```
