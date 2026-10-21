# Affine Cipher

- CodeNet ID: `p00040`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

One of the simple encryption methods is called the Affine Cipher. First, the alphabet letters a–z are replaced by numbers from 0 to 25 as a = 0, b = 1, c = 2, ..., x = 23, y = 24, z = 25. Then, the letters of the original text are replaced using the following formula:

$F(\gamma) = (\alpha \cdot \gamma + eta) \pmod{26}$

Here, mod 26 represents the remainder when divided by 26. For example, when $\\alpha = 3, \beta = 2$, the letter 'a' (=0) is replaced by $F(0) = (3 \cdot 0 + 2) \pmod{26} = 2$, which is 'c', and the letter 'n' (=13) is replaced by $F(13) = (3 \cdot 13 + 2) \pmod{26} = 15$, which is 'p'.
In this process, it is assumed that $\\alpha$ and $\beta$ are carefully chosen so that $F(\\gamma)$ for a given $\\gamma$ always results in a one-to-one mapping (the condition is that $\\alpha$ and 26 must be coprime). This ensures that cases like $\\alpha = 4, \beta = 7$, where $F('a') = 7$ and $F('n') = 7$ (both 'a' and 'n' are replaced by the same 'h'), do not occur. Additionally, characters other than alphabet letters are not replaced.

Please create a program that decrypts an encrypted string back into the original text. The original text is guaranteed to contain one of the following as a keyword:

```text
that
this
```

## Input

Multiple datasets are provided. The first line contains the number of datasets $n$ ($n \leq 30$). Following this, $n$ lines of data are provided. Each dataset consists of one line containing an encrypted text of up to 256 characters, consisting of lowercase English letters and spaces.

## Output

For each dataset, output the decrypted original text on a single line.

## Sample Input 1

```text
1
y eazqyp pnop pngtg ye obmpngt xmybp mr lygw
```

## Output for the Sample Input 1

```text
i submit that there is another point of view
```
