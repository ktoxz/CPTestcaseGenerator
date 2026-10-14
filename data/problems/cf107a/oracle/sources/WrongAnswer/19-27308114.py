n, p = list(map(int, input().split(' ')))

sets = []
mins = []
init = []
fnit = []

def find_in_sets(a):
    for i, _set in enumerate(sets):
        if a in _set:
            return i
    return None

for i in range(p):
    a, b, d = list(map(int, input().split(' ')))

    set_a = find_in_sets(a)
    set_b = find_in_sets(b)

    if set_a == None and set_b != None:
        sets[set_b].add(a)
        mins[set_b] = min(mins[set_b], d)
        init[set_b] = a
    elif set_b == None and set_a != None:
        sets[set_a].add(b)
        mins[set_a] = min(mins[set_a], d)
        fnit[set_a] = b
    elif set_a != set_b:
        sets[set_a] = sets[set_a] | sets[set_b]
        mins[set_a] = min(mins[set_a], mins[set_b], d)
        if a == fnit[set_a]:
            fnit[set_a] = fnit[set_b]
        else:
            init[set_a] = init[set_b]
        del init[set_b]
        del fnit[set_b]
        del sets[set_b]
        del mins[set_b]
    else:
        sets.append(set([a, b]))
        mins.append(d)
        init.append(a)
        fnit.append(b)

sols = []
print(len(mins))
for i, f, m in zip(init, fnit, mins):
    sols.append((i, f, m))

sols.sort()
for i, f, m in sols:
    print(i, f, m)