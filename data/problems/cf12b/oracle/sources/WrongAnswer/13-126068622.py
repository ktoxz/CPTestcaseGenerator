d = {}
for i in input().strip():
    i = int(i)
    if i in d:
        d[i] += 1
    else:
        d[i] = 1
f = ''
for i in [1,2,3,4,5,6,7,8,9]:
    if i in d:
        d[i] -= 1
        f += str(i)
        break
for i in sorted(d):
    f += str(i) * d[i]
if int(f) == int(input()):
    print('OK')
else:
    print('WRONG_ANSWER')