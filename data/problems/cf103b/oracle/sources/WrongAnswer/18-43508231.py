v, e = map(int, input().split())
E, V = [], set()

for _ in range(e):
    a, b = map(int, input().split())
    V.add(a)
    V.add(b)
    E.append([a, b])

sets = [ set([vertex]) for vertex in V ]

def getSet(vertex):
    for s in sets:
        if vertex in s: return s

in_tree = 0

for edge in E:
    a, b = edge
    if a in V: V.remove(a)
    if b in V: V.remove(b)
    sa, sb = getSet(a), getSet(b)

    if sa.isdisjoint(sb):
        in_tree += 1
        sa |= sb
        sets.remove(sb)

print('FHTAGN!' if in_tree == len(E) - 1 and len(V) == 0 else 'NO')