# Vegetable Garden

- CodeNet ID: `p00253`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

You have decided to plant vegetables in your home garden. Since you had $n$ seeds, you planted them one by one over $n$ days. Every seed sprouted and is growing steadily. You are looking forward to the harvest time.

One day, while watering the seedlings as usual, you noticed something strange. There should be $n$ vegetable seedlings, but there is one extra. A weed has grown. You want to pull it out immediately, but unfortunately, all the seedlings look very similar, and you cannot distinguish between the vegetables and the weed.

The only clue is the growth rate of the vegetables. These vegetables continue to grow by a fixed length every day from the moment they are planted. However, you do not know how many centimeters this "fixed length" is. Additionally, you have forgotten how many days ago you planted the first seed. The seedlings are arranged in a row, and the only thing you remember is that you planted the seeds one by one from right to left every day.

Write a program that takes the lengths of the $n+1$ seedlings as input and outputs the length of the weed.

## Input

The input consists of multiple data sets. The end of the input is indicated by a single line containing zero. The input is given in the following format:

```text
n
h1 h2 h3 ... hn+1
```

The integer $n$ ($4 \le n \le 100$) on the first line represents the number of vegetable seedlings. The second line contains $n+1$ integers separated by single spaces, where $h_i$ ($1 \le h_i \le 10^9$) represents the length of the $i$-th seedling from the left.

Input where $h_1, h_2, \dots, h_{n+1}$ form an arithmetic progression will not be given.

The number of data sets does not exceed 500.

## Output

For each data set, output the length of the weed.

## Sample Input 1

```text
5
1 2 3 6 4 5
6
1 3 6 9 12 15 18
4
5 7 9 11 12
0
```

## Output for the Sample Input 1

```text
6
1
12
```
