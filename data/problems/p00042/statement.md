# Thief

- CodeNet ID: `p00042`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

A thief has sneaked into a museum containing many treasures, carrying only one large wrapping cloth. Although there are many items they wish to steal, the weight the wrapping cloth can withstand is limited; if this limit is exceeded, the cloth will tear. Therefore, the thief must determine a combination of treasures that maximizes the total value without tearing the wrapping cloth.

Given the weight $W$ that the wrapping cloth can withstand, and the value and weight of each treasure in the museum, create a program that outputs the total value and the total weight when the total value is maximized such that the sum of the weights does not exceed $W$. If there are multiple combinations that result in the maximum total value, the one with the smaller total weight should be output.

## Input

Multiple datasets are provided. Each dataset is given in the following format:

```text
W
N
v1,w1
v2,w2
:
vN,wN
```

The first line contains an integer $W$ ($W \le 1,000$) representing the weight the wrapping cloth can withstand, and the second line contains the number of treasures $N$ ($1 \le N \le 1,000$). The following $N$ lines each contain a pair of integers: $v_i$ ($0 \le v_i \le 10,000$), representing the value of the $i$-th treasure, and $w_i$ ($0 \le w_i \le W$), representing its weight.

Input ends when $W$ is 0. The number of datasets does not exceed 50.

## Output

For each dataset, output as follows:

```text
Case dataset_number:
maximum total treasure value
total treasure weight for that solution
```

## Sample Input 1

```text
50
5
60,10
100,20
120,30
210,45
10,4
50
5
60,10
100,20
120,30
210,45
10,4
0
```

## Output for the Sample Input 1

```text
Case 1:
220
49
Case 2:
220
49
```
