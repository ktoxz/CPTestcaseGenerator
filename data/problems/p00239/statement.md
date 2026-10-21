# Calorie Calculation

- CodeNet ID: `p00239`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Foods contain three nutrients known as the three major nutrients: "protein," "fat," and "carbohydrates." Per 1g (gram), protein and carbohydrates are calculated as 4 kcal (kilocalories), and fat is calculated as 9 kcal. For example, according to the table below, cake number 1 contains 7g of protein, 14g of fat, and 47g of carbohydrates. Based on this, the calories contained are calculated as 4 × 7 + 9 × 14 + 4 × 47 = 342 kcal. Others are calculated in the same way.

Given the number of snacks $n$ to be classified, the information for each snack, and the restriction information, create a program that outputs a list of snacks that do not exceed the restrictions if eaten alone (i.e., snacks that are okay to eat).

Snack information consists of the snack number $s$, the weight of protein $p$ contained in that snack, the weight of fat $q$, and the weight of carbohydrates $r$. The restriction information consists of the maximum allowable weight of protein $P$, fat $Q$, carbohydrates $R$, and the maximum allowable calorie intake $C$. If any one of the protein, fat, carbohydrates, or calories exceeds the limit, it is a restriction violation and is judged as a "snack that must not be eaten."

For the list of snacks that are okay to eat, output the numbers of the snacks that are okay to eat in the order they were input. If there are no snacks that are okay to eat, output "NA".

Regarding the 4 snacks in the table above, if the restrictions are $P = 10, Q = 15, R = 50, C = 400$, the cake and pudding are classified as snacks that are okay to eat because their respective nutrients and calories are below the limit values, but the potato chips are classified as snacks that must not be eaten because their carbohydrates and calories exceed the limit values, and the dorayaki is classified as a snack that must not be eaten because its carbohydrate amount exceeds the limit value.

## Input

A sequence of multiple datasets is given. The end of the input is indicated by a single line containing zero. Each dataset is given in the following format:

```text
n
s1 p1 q1 r1
s2 p2 q2 r2
:
sn pn qn rn
P Q R C
```

The first line gives the number of snacks $n$ ($1 \le n \le 1000$). The following $n$ lines give the number of the $i$-th snack $s_i$ ($1 \le s_i \le 1000$), and integers $p_i, q_i, r_i$ ($0 \le p_i, q_i, r_i \le 100$) representing the weight of each nutrient.

The following line gives integers $P, Q, R$ ($0 \le P, Q, R \le 100$) and $C$ ($0 \le C \le 1700$) representing the limit values for each nutrient and calories.

The number of datasets does not exceed 100.

## Output

For each dataset, output the numbers of the snacks that are okay to eat, or "NA".

## Sample Input 1

```text
4
1 7 14 47
2 5 35 55
3 6 3 59
4 6 5 15
10 15 50 400
2
1 8 10 78
2 4 18 33
10 10 50 300
0
```

## Output for the Sample Input 1

```text
1
4
NA
```
