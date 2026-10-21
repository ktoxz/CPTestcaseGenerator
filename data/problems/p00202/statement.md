# Boss's Treat

- CodeNet ID: `p00202`
- Dataset: `AIZU`
- Time limit: `5000 ms`
- Memory limit: `131072 KB`

Taro Aizu's company has a boss who hates things that cannot be divided evenly. Whenever Taro goes out to eat with this boss, they usually split the bill; however, if the total payment amount is not divisible by the number of participants, the boss always treats everyone.

One day, Taro became the organizer of a dinner party. Being short on money, Taro wondered if he could somehow invite the boss and get him to treat everyone. He must place the order with the restaurant soon, but since he does not yet know how many people will participate, he wants to order an amount that is not divisible by any possible number of participants.

You, a colleague of Taro who is also planning to attend the dinner party, decided to help Taro by calculating the maximum total amount within the budget that is not divisible by any integer (excluding 1 and the total amount itself).

Given the types of dishes, the price of each dish, and the budget, create a program that outputs the maximum total amount less than or equal to the budget that is not divisible by any integer (excluding 1 and the total amount itself). Note that multiple quantities of each type of dish can be ordered, and it is not necessary to order every type of dish. If no such total amount exists, output NA.

## Input

Multiple datasets are given as input. The end of the input is indicated by two lines of zeros.
Each dataset is given in the following format:

```text
n x
v1
v2
:
vn
```

The first line contains the number of dish types $n$ ($1 \le n \le 30$) and the budget $x$ ($1 \le x \le 1,000,000$), separated by a space. The following $n$ lines each contain an integer $v_i$ ($1 \le v_i \le 1,000,000$) representing the price of the $i$-th type of dish.

The number of datasets does not exceed 100.

## Output

For each input dataset, output the total amount closest to the budget (the maximum possible), or NA, on a single line.

## Sample Input 1

```text
4 15000
305
260
129
500
3 400
10
20
30
3 200909
5
9
12
0 0
```

## Output for the Sample Input 1

```text
14983
NA
200909
```
