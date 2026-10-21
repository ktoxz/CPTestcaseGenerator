# Customer Appreciation Festival

- CodeNet ID: `p00227`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Amidst continuing bad weather and soaring vegetable prices, Seven Mart is holding a bulk-buying sale for its customers. Since vegetables that are rarely on the shelves can be obtained at affordable prices, the store is very crowded.

One day, a group of three close friends living in Matsunaga Housing were chatting excitedly while holding a Seven Mart advertisement. As this sale is branded as the "Customer Appreciation Festival," the main attraction is that the cheapest item among the vegetables packed in a bag becomes free. Reading the advertisement, the sale seems to be as follows:

- Up to $m$ vegetables can be packed into one bag.

- For a bag packed with exactly $m$ vegetables, the cheapest vegetable among them becomes free.

- Bags containing fewer than $m$ vegetables are not eligible for the discount.

The three friends immediately went shopping at Seven Mart.

After shopping, the three met outside the store. While talking and feeling satisfied that they were able to buy many things cheaply, they realized that all three of them had purchased the same vegetables. One of them said, "It's really cheap, isn't it? It only cost XXX yen!" Another replied in surprise, "Eh? Mine was ** yen more expensive than that! Why?" Meanwhile, the remaining person looked at their receipt and noticed that they had purchased them for the lowest price.

Now, how should the vegetables be packed into bags to make the purchase price the lowest? Given the number of vegetables to be purchased, the number of vegetables that can fit in a bag, and the price of each vegetable, create a program that outputs the minimum purchase price.

## Input

A sequence of multiple datasets is given as input. The end of the input is indicated by two lines of zeros.
Each dataset is given in the following format:

```text
n m
p1 p2 ... pn
```

The first line contains the number of vegetables to be purchased $n$ ($1 \le n \le 1000$) and the number of vegetables that can fit in a bag $m$ ($1 \le m \le 1000$). The second line contains the price of each vegetable $p_i$ ($10 \le p_i \le 10000$).

The number of datasets does not exceed 100.

## Output

For each input dataset, output the minimum purchase price on one line.

## Sample Input 1

```text
4 2
50 40 100 80
7 3
400 300 100 700 200 600 500
0 0
```

## Output for the Sample Input 1

```text
150
2100
```
