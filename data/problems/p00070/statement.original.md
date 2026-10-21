# Combination of Number Sequences

- CodeNet ID: `p00070`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

0 から 9 までの整数を使った n 個の数の並び k1, k2, ..., kn を考えます。正の整数 n と s を読み込んで、

k1 + 2 × k2 + 3 × k3 + ... + n × kn = s

となっているような n 個の数の並びが何通りあるかを出力するプログラムを作成してください。ただし、1 つの「n 個の数の並び」には同じ数が 2 回以上現われないものとします。

## Input

入力は複数のデータセットからなります。各データセットとして、n (1 ≤ n ≤ 10) と s (0 ≤ s ≤ 10,000)が空白区切りで１行に与えられます。

データセットの数は 100 を超えません。

## Output

データセットごとに、n 個の整数の和が s になる組み合わせの個数を１行に出力します。

## Sample Input 1

```text
3 10
3 1
```

## Output for the Sample Input 1

```text
8
0
```
