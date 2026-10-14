# A. Palindromic Times

Source: https://codeforces.com/contest/108/problem/A

A. Palindromic Times
time limit per test
2 seconds
memory limit per test
256 megabytes
input
standard input
output
standard output

Tattah is asleep if and only if Tattah is attending a lecture. This is a well-known formula among Tattah's colleagues.
On a Wednesday afternoon, Tattah was attending Professor HH's lecture. At 12:21, right before falling asleep, he was staring at the digital watch around Saher's wrist. He noticed that the digits on the clock were the same when read from both directions i.e. a palindrome.
In his sleep, he started dreaming about such rare moments of the day when the time displayed on a digital clock is a palindrome. As soon as he woke up, he felt destined to write a program that finds the next such moment.
However, he still hasn't mastered the skill of programming while sleeping, so your task is to help him.

Input
The first and only line of the input starts with a string with the format "HH:MM" where "HH" is from "00" to "23" and "MM" is from "00" to "59". Both "HH" and "MM" have exactly two digits.

Output
Print the palindromic time of day that comes soonest after the time given in the input. If the input time is palindromic, output the soonest palindromic time after the input time.

## Examples

## Sample Input 1
```text
12:21
```

## Output for the Sample Input 1
```text
13:31
```

## Sample Input 2
```text
23:59
```

## Output for the Sample Input 2
```text
00:00
```
