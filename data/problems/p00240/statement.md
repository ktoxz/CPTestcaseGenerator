# Interest Calculation

- CodeNet ID: `p00240`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Interest is paid on money deposited in a bank, and the calculation methods and interest rates vary by bank. The sum of the interest and the principal is called the total amount. There are two methods for calculating the total amount: "simple interest," where interest is calculated without adding it to the principal, and "compound interest," where interest is added to the principal for subsequent calculations. To obtain a larger total amount, one must understand this difference. The calculation methods for the total amount are as follows:

![Problem diagram 1](images/01.png)

![Problem diagram 2](images/02.png)

Given the number of banks, the number of years the money is deposited, and information for each bank (bank number, type of interest, and annual interest rate (percent)), create a program that outputs the bank number that results in the highest total amount. It is guaranteed that there is only one bank that yields the highest total amount.

## Input

Multiple datasets are provided. The end of the input is indicated by a single zero. Each dataset is given in the following format:

```text
n
y
b1 r1 t1
b2 r2 t2
:
bn rn tn
```

The first line contains the number of banks $n$ ($1 \le n \le 50$), and the second line contains the number of years the money is deposited $y$ ($1 \le y \le 30$). The following $n$ lines contain the bank number $b_i$, the annual interest rate represented by an integer $r_i$ ($1 \le r_i \le 100$), and the type of interest $t_i$ (1 or 2) for the $i$-th bank. The type of interest $t_i$ is given as 1 for simple interest and 2 for compound interest.

The number of datasets does not exceed 100.

## Output

For each dataset, output the bank number that results in the highest total amount on a single line.

## Sample Input 1

```text
2
8
1 5 2
2 6 1
2
9
1 5 2
2 6 1
0
```

## Output for the Sample Input 1

```text
2
1
```
