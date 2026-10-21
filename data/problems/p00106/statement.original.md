# Discounts of Buckwheat

- CodeNet ID: `p00106`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Aizu is famous for its buckwheat. There are many people who make buckwheat noodles by themselves.

One day, you went shopping to buy buckwheat flour. You can visit three shops, A, B and C. The amount in a bag and its unit price for each shop is determined by the follows table. Note that it is discounted when you buy buckwheat flour in several bags.

For example, when you buy 12 bags of flour at shop A, the price is reduced by 20 % for 10 bags, but not for other 2 bags. So, the total amount shall be (380 × 10) × 0.8 + 380 × 2 = 3,800 yen.

Write a program which reads the amount of flour, and prints the lowest cost to buy them. Note that you should buy the flour of exactly the same amount as the given input.

## Input

The input consists of multiple datasets. For each dataset, an integer a (500 ≤ a ≤ 5000, a is divisible by 100) which represents the amount of flour is given in a line.

The input ends with a line including a zero. Your program should not process for the terminal symbol. The number of datasets does not exceed 50.

## Output

For each dataset, print an integer which represents the lowest cost.

## Sample Input 1

```text
500
2200
0
```

## Output for the Sample Input 1

```text
850
3390
```
