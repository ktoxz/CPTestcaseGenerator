# A. Romaji

Source: https://codeforces.com/contest/1008/problem/A

A. Romaji
time limit per test
2 seconds
memory limit per test
256 megabytes
input
standard input
output
standard output

Vitya has just started learning Berlanese language. It is known that Berlanese uses the Latin alphabet. Vowel letters are "a", "o", "u", "i", and "e". Other letters are consonant.
In Berlanese, there has to be a vowel after every consonant, but there can be any letter after any vowel. The only exception is a consonant "n"; after this letter, there can be any letter (not only a vowel) or there can be no letter at all. For example, the words "harakiri", "yupie", "man", and "nbo" are Berlanese while the words "horse", "king", "my", and "nz" are not.
Help Vitya find out if a word $$$s$$$ is Berlanese.

Input
The first line of the input contains the string $$$s$$$ consisting of $$$|s|$$$ ($$$1\leq |s|\leq 100$$$) lowercase Latin letters.

Output
Print "YES" (without quotes) if there is a vowel after every consonant except "n", otherwise print "NO".
You can print each letter in any case (upper or lower).

## Examples

## Sample Input 1
```text
sumimasen
```

## Output for the Sample Input 1
```text
YES
```

## Sample Input 2
```text
ninja
```

## Output for the Sample Input 2
```text
YES
```

## Sample Input 3
```text
codeforces
```

## Output for the Sample Input 3
```text
NO
```
