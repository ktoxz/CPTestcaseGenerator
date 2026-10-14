# Submitted using https://github.com/Nirlep5252/codeforces-cli
# >.<

s = input()
k = int(input())

c = {a: s.count(a) for a in set(s)}
chars_freq = c.copy()
uwu = sorted(chars_freq.items(), key = lambda x: x[1])

for e, i in uwu:
    if i <= k:
        k -= i
        del chars_freq[e]
    else:
        chars_freq[e] = i - k
        k = 0
        break

toprint = len(s)
ans = ""

for e, i in chars_freq.items():
    ans += e * i
    toprint -= i

if toprint:
    for e, i in chars_freq.items():
        diff = c[e] - chars_freq[e]
        if diff <= toprint:
            ans += e * diff
            toprint -= diff
        else:
            ans += e * (toprint)
            toprint = 0

print(len(set(ans)))
print(ans)