# Input Candidates

- CodeNet ID: `p00242`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Mobile phones are equipped with a function to display input candidates to efficiently enter text, such as emails. This function records words that are used frequently and suggests words that start with the entered character as input candidates. For example, if you usually enter the word "computer" often, just entering "c" will suggest "computer" as a candidate. Let's create the basic part of such a function.

Given a text and a character, create a program that outputs words starting with that character in descending order of their frequency of occurrence. However, if there are multiple words with the same frequency, output them in lexicographical order. Output up to a maximum of 5 words. If no corresponding words exist, output "NA".

## Input

Multiple datasets are given. The end of the input is represented by a single zero. Each dataset is given in the following format:

```text
n
line1
line2
:
linen
k
```

On the first line, the number of lines of text $n$ ($1 \le n \le 10$) is given. The following $n$ lines contain the text. The text consists of half-width lowercase English letters and half-width spaces, and the number of characters per line is between 1 and 1024 characters inclusive. Words separated by spaces are between 1 and 20 characters inclusive.

On the following line, the starting character $k$ is given as a half-width English letter.

The number of datasets does not exceed 100.

## Output

For each dataset, output the words starting with the specified character, or "NA".

## Sample Input 1

```text
1
ben likes bananas the best among many fruits because bananas are sweet and cheap
b
1
winners get to visit aizu and the university of aizu and make many friends as well
a
3
ask alex about
the answer for the
assignment on android apps
a
2
programming is both
a sport and an intellectual puzzle
c
0
```

## Output for the Sample Input 1

```text
bananas because ben best
aizu and as
about alex android answer apps
NA
```
