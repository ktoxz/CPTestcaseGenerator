isPal = lambda h, m: str(h) == str (m % 10 * 10 + int (m / 10))

def Inc (h, m):
    m += 1
    if m == 60:
        m = 0
        h += 1
        if h == 24:
            h = 0
    return [h, m]

def Tr (s):
    if len(s) == 1:
        s = '0' + s[0]
    return s

h, m = [int(i) for i in input().split(':')]
h, m = Inc (h, m)
while (not isPal (h, m)):
    h, m = Inc (h, m)

print (Tr (str(h)) + ':' + Tr (str(m)))