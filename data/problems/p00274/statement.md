# Matching Prizes

- CodeNet ID: `p00274`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Joe and Yae are a close couple. Joe collects prizes from capsule toy vending machines (gachapon), and even when they go out together, he is so enthusiastic that he will try them several times whenever he finds one. Yae used to just watch Joe having fun by his side, but she decided to give him a gachapon prize as his next birthday present. Yae herself is not very interested in gachapon, but if possible, she wants a prize that matches Joe's.

In the gachapon Yae is considering trying, one prize is obtained per challenge. She knows how many types of prizes there are (including those that are sold out) and how many of each prize remain. However, she does not know which prize will come out in a single challenge. Therefore, please create a program that outputs the minimum number of challenges required for Yae to be guaranteed to obtain two of the same prize, regardless of the order in which the prizes appear.

## Input

The input consists of multiple datasets. The end of the input is indicated by a single line containing zero. Each dataset is given in the following format:

```text
N
k1 k2 ... kN
```

Each dataset consists of 2 lines. The first line contains an integer $N$ ($1 \le N \le 10000$) representing the number of types of prizes. The following line contains integers $k_i$ ($0 \le k_i \le 10000$) representing how many of each prize remain.

The number of datasets does not exceed 100.

## Output

For each dataset, output the minimum number of challenges required to be guaranteed to obtain two of the same prize. If it is impossible, output NA.

## Sample Input 1

```text
2
3 2
3
0 1 1
1
1000
0
```

## Output for the Sample Input 1

```text
3
NA
2
```

In the first dataset, although it is possible to finish in 2 challenges if the first or second type of prize appears consecutively by luck, 3 challenges are necessary to be guaranteed to obtain two of the same type of prize.
In the second dataset, it is impossible because there are no prizes that have two or more remaining.
In the third dataset, there is only one type of prize, so 2 challenges will guaranteedly yield two of that prize.
