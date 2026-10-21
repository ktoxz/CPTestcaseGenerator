# Kobuta Nuki Tsune Ko

- CodeNet ID: `p00225`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

A-ko's relative, B-o, has come to visit her house. He is 3 years old and loves singing. He is singing a song he learned in kindergarten called "Kobuta Nuki Tsune Ko" (lyrics and composition by Naozumi Yamamoto) with all his might. In this song, four words "kobuta", "tanuki", "kitsune", and "neko" form a shiritori chain in order, and furthermore, the last sound and the first sound are the same. B-o asked A-ko to tell him whether a similar shiritori chain can be made from the words he says.

Therefore, to help A-ko, let's create a program that determines whether it is possible to use all of the given words to form a shiritori chain such that the first character of the first word and the last character of the last word are the same.

Given $n$ words as input, create a program that determines whether a shiritori chain can be created from those words; output OK if it is possible, and NG if it is impossible.

## Input

A sequence of multiple datasets is given as input. The end of the input is indicated by a single line containing zero.
Each dataset is given in the following format:

```text
n
word1
word2
:
wordn
```

The first line contains the number of words $n$ ($2 \le n \le 10000$). The following $n$ lines contain $n$ words $word_i$ (strings consisting only of half-width lowercase English letters of 32 characters or less).

The number of datasets does not exceed 50.

## Output

For each input dataset, output the determination result on one line.

## Sample Input 1

```text
5
apple
yellow
georgia
king
email
7
apple
yellow
georgia
king
email
wink
lucky
0
```

## Output for the Sample Input 1

```text
NG
OK
```
