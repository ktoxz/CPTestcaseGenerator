# When will the trip be?

- CodeNet ID: `p00206`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

You want to go on a trip with your friend. However, your friend has a habit of spending too much and is unable to save up for the trip expenses. If your friend continues their current lifestyle, it is unclear when you will finally be able to go on the trip. Therefore, wanting to go on the trip as soon as possible, you decided to create a program to help your friend save money systematically.

If your friend's allowance for a certain month is $M$ yen and the amount they spend in that month is $N$ yen, then $(M - N)$ yen is saved for that month. Given the monthly income and expenditure information $M$ and $N$, create a program that outputs the number of months it takes for the total savings to reach the trip expense $L$. However, if the savings do not reach the trip expense even after 12 months, output NA.

## Input

A sequence of multiple datasets is given as input. The end of the input is indicated by a single line containing zero.
Each dataset is given in the following format:

```text
L
M1 N1
M2 N2
:
M12 N12
```

The first line contains the trip expense $L$ ($1 \le L \le 1000000$, integer). The following 12 lines contain the income and expenditure information for the $i$-th month, $M_i$ and $N_i$ ($0 \le M_i, N_i \le 100000, N_i \le M_i$, integers).

The number of datasets does not exceed 1000.

## Output

For each input dataset, output the number of months it takes for the savings to reach the trip expense on a single line.

## Sample Input 1

```text
10000
5000 3150
5000 5000
0 0
5000 1050
5000 3980
5000 210
5000 5000
5000 5000
0 0
5000 2100
5000 2100
5000 2100
29170
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 100000
100000 70831
0
```

## Output for the Sample Input 1

```text
6
NA
```
