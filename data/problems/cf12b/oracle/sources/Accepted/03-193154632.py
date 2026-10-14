# LUOGU_RID: 101915677
t = ''.join(sorted(input()))
k = t.rfind('0') + 1
if k and len(t) > 1:
    t = t[k] + t[:k] + t[k+1:]
print(t == input() and 'OK' or 'WRONG_ANSWER')