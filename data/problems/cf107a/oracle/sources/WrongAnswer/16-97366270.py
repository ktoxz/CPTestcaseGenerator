n, p = map(int, input().split(" "))

adj_map = {}
adj_in = [0] * (n + 1)
for i in range(p):
    a, b, d = map(int, input().split(" "))
    adj_map[a] = (b, d)
    adj_in[b] += 1

pipes = []
for i in range(1, n + 1):
    if adj_in[i] == 0:
        s = i
        mp = 10 ** 6 + 1
        e = -1
        while True:
            if adj_map.get(s, False):
                mp = min(mp, adj_map[s][1])
                s = adj_map[s][0]
            else:
                e = s
                break
        pipes.append((i, e, mp))

print(len(pipes))
for pipe in sorted(pipes):
    print("{} {} {}".format(*pipe))