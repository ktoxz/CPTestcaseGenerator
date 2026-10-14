#problem15
"""def ucitajDuzinu():
    return int(input())


def ucitajBroj():
    return input()


def zadatak(d, b):
    s1 = 0
    s2 = 0
    for i in range(d//2):
        if (int(b[i]) == 7 or b[i] == '4') and (b[d - 1 - i] == '7' or b[d - 1 - i] == '4'):
            s1 += int(b[i])
            s2 += int(b[d - 1 - i])
        else:
            return False
    return s1 == s2


def ispis(b):
    if b:
        print('YES', end="")
    else:
        print('NO', end="")


duzina = ucitajDuzinu()
broj = ucitajBroj()
ispis(zadatak(duzina, broj))"""

"""def ucitajMehanizam():
    meh = []
    for i in range(4):
        meh.append(int(input()))
    meh.append(int(input()))
    return meh

#problem14
def izracunaj(meh):
    osakaceni = 0
    pom = []
    for i in range(meh[-1]):
        pom.append(0)
    for i in range(4):
        j = meh[i] - 1
        while j < meh[-1]:
            if pom[j] == 0:
                osakaceni += 1
                pom[j] = 1
            j += meh[i]
    return osakaceni


udarci = ucitajMehanizam()
br = izracunaj(udarci)
print(br, end="")"""

#problem16

"""def ucitaj():
    ls = []
    for i in range(3):
        ls.append(input())
    return ls


def zadatak(ls):
    t = list(ls[0] + ls[1])
    t = sorted(t)
    p = sorted(list(ls[2]))
    if len(t) != len(p):
        return False
    else:
        for i in range(len(t)):
            if t[i] != p[i]:
                return False
        return True


def ispis(ls):
    if zadatak(ls):
        print('YES', end='')
    else:
        print('NO', end='')


imena = ucitaj()
ispis(imena)"""


#problem17
"""def unos():
    n = int(input())
    l = [int(i) for i in input().split()]
    return l


def zadatak(l):
    mini = l[-1]
    inmin = -1
    maks = l[0]
    inmaks = 0
    for i in range(len(l)):
        if l[i] > maks:
            maks = l[i]
            inmaks = i
        if l[-1-i] < mini:
            mini = l[-1-i]
            inmin = -1 - i
    suma = inmaks + abs(inmin) - 1
    if inmaks > len(l) + inmin:
        suma -= 1
    return suma


def ispis(l):
    print(zadatak(l), end='')


red = unos()
ispis(red)"""


"""def zad(tekst):
    tekst = sorted(tekst)
    recnik = {}
    for i in tekst:
        if i in recnik:
            recnik[i] += 1
        else:
            recnik[i] = 1
    s = ""
    for i in recnik:
        s += "'" + i + "'" + ":" + str(recnik[i]) + ", "
    print(s[0:-2])


tekst = "abcdfeg"
zad(tekst)"""
#zadatak18
"""def ucitaj():
    n = int(input())
    s = [int(i) for i in input().split()]
    return s


def zadatak(s):
    pom = [i for i in s]
    for i in range(len(s)):
        pom[s[i] - 1] = i + 1
    return pom


def ispis(s):
    print(*s)


drugari = ucitaj()
ispis(zadatak(drugari))"""


def ucitaj():
    s = [int(i) for i in input().split()]
    return s


def nzd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def zadatak(s):
    while s[2] > 0:
        if s[2] >= s[0]:
            s[2] -= nzd(s[2], s[0])
        else:
            print(1)
            break
        if s[2] >= s[1]:
            s[2] -= nzd(s[2], s[1])
        else:
            print(0)
            break
    else:
        print(1)


lin = ucitaj()
zadatak(lin)