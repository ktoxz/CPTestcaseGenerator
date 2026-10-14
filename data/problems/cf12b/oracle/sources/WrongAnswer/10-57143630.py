"""
One cold winter evening Alice and her older brother Bob was sitting at home near the fireplace and giving each other interesting problems to solve. When it was Alice's turn, she told the number n to Bob and said:

—Shuffle the digits in this number in order to obtain the smallest possible number without leading zeroes.

—No problem! — said Bob and immediately gave her an answer.

Alice said a random number, so she doesn't know whether Bob's answer is correct. Help her to find this out, because impatient brother is waiting for the verdict.

Input
The first line contains one integer n (0 ≤ n ≤ 109) without leading zeroes. The second lines contains one integer m (0 ≤ m ≤ 109) — Bob's answer, possibly with leading zeroes.

Output
Print OK if Bob's answer is correct and WRONG_ANSWER otherwise.
"""

q = list(map(int, list(input())))
q_set = set(q)

a = input()

verdict = True
# {'correct': "OK", 'false': "WRONG_ANSWER"}

if len(q) == 1:
    print("OK" if int(a) == q[0] else "WRONG_ANSWER")

else:
    answer  = ''

    has_zero = 0 in q_set
    if has_zero:
        q_set.remove(0)
        answer += '0' * q.count(0)

    min_elm = min(q_set)
    q_set.remove(min_elm)
    answer = str(min_elm)* q.count(min_elm) + answer

    while q_set:
        min_elm = min(q_set)
        q_set.remove(min_elm)
        answer += str(min_elm)*q.count(min_elm)

    print("OK" if a == answer else "WRONG_ANSWER")