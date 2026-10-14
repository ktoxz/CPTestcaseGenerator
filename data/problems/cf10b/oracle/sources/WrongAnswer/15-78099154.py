def find_avaible(size):
    pos = []
    for i in range(k):
        j = 0
        c = 0
        while j < k:
        #    print('pos',pos)
        #    print('j' , j)

            if th[i][j] == 0:
                c += 1
                if c == 1:
                    start = j

                if c == size:
                    end = j
                    pos.append([i+1, start+1, end+1])
                    if size != 1:
                        j -= 1
                    c = 0
            else:
                c = 0
            j += 1


    #print ('pos', pos)

    if len(pos) == 0:
        return -1
    else:
        return pos

# row, yl, yr,
# [[1, 1, 2], [1, 2, 3], [2, 1, 2], [2, 2, 3], [3, 1, 2], [3, 2, 3]]
# [[0, 1, 1], [1, 1, 0], [2, 0, 1], [3, 0, 0], [4, 1, 1], [5, 1, 0]]
def find_dist(arr, i):
    dist = []
    dist_x = abs(arr[0] - center)
    dist_y = abs(arr[1] - center)
    dist = [dist_x, dist_y, i]
    return dist


def closest(ok, size):
    dists = []
    for i in range(len(ok)):
        d = find_dist(ok[i], i)
        dists.append(d)

    #print('dis',dists)
    if size == 1:
        dists.sort(key = lambda x: (x[0], x[1]))
    else:
        dists.sort(key = lambda x: x[0])

    #print('sor', dists)
    best = dists[0][2]
    #print(best)
    places = ok[best]
    #print(places)
    return places

def buy(places):
    global th
    #print('range', places[1]-1)
    #print('range', places[2]-1)
    for i in range(places[1]-1, places[2]):
        th[places[0]-1][i] = 1

    #print(th)


n ,k = map(int, input().split())
m = list(map(int, input().split()))
#print(m)
r = c = k
th = [[0 for x in range(r)] for y in range(c)]
#print(th)
center = (k+1) // 2
#print('center', center)

res = []
for i in range(len(m)):
    p = find_avaible(m[i])
    if p == -1:
        print(-1)
    else:
        c = closest(p , m[i])
        print(*c, sep= ' ')
        buy(c)