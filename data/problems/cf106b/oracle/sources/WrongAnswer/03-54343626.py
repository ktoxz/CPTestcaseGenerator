#  =========     /\       /|    |====/|
#      |        /  \       |    |   / |
#      |       /____\      |    |  /  |
#      |      /      \     |    | /   |
#  ========= /        \  =====  |/====|  
#  code

if __name__ == "__main__":
    p = []
    c = []
    r = []
    n = int(input())
    x = range(n)
    i = 0
    for i in x:
        a,b,e,d = map(int,input().split())
        c.append(d)
        p.append((a,b,e))
    
    for i in x:
        for j in x:
            if p[j] < p[i]:
                r.append(j)

    for i in r:
        c[i] = 1000000
    print(c.index(min(c)) + 1)