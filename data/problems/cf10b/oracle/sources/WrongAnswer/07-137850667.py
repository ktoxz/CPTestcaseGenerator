def foundDistance(k, row, l, r):
    e = abs(k // 2 - row) * (r - l + 1)
    for i in range(l, r + 1):
        e += abs(k // 2 + 1 - i)
    #print(k//2, row, l, r, "distance=", e)
    return e


n, k = map(int, input().split())
a = list(map(int, input().split()))

free = [[[1, k]] for i in range(k)]

order = [i for i in range(k)]

for i in range(n):
    found = False
    take_middle = False
    row, l, r = 10000, 0, 0
    need_place = a[i]
    distance = 10 ** 10
    ind = 0
    new_segment = []
    middle_save = []

    #print(free)

    for j in order:
        if free[j] == [[]]:
            continue
        for place in free[j]:
            left = place[0]
            right = place[1]

            if right - left + 1 >= need_place:
                found = True

                if left == 1 and right == k:
                    new_distance = foundDistance(k, j, k // 2 + 1 - need_place // 2, k // 2 + 1 + (need_place - 1) // 2)
                    if new_distance < distance:
                        take_middle = True
                        distance = new_distance
                        middle_save = [j, k // 2 + 1 - need_place // 2, k // 2 + 1 + (need_place - 1) // 2]

                else:
                    if right < k / 2:
                        new_distance = foundDistance(k, j, right - need_place + 1, right)
                        if new_distance < distance:
                            take_middle = False
                            distance = new_distance
                            row, l, r = j, right - need_place + 1, right
                            ind = free[j].index(place)
                            if right - left + 1 > need_place:
                                new_segment = [1, right - 1]

                    else:
                        new_distance = foundDistance(k, j, left, left + need_place - 1)
                        if new_distance < distance:
                            take_middle = False
                            distance = new_distance
                            row, l, r = j, left, left + need_place - 1
                            ind = free[j].index(place)
                            if right - left + 1 > need_place:
                                new_segment = [right + 1, k]

    if found:
        if take_middle:
            row, l, r = middle_save
            if need_place == k:
                free[row] = [[]]
            elif need_place == k - 1:
                free[row] = [[k, k]]
            else:
                free[row] = [[1, l - 1], [r + 1, k]]
        else:
            free[row].pop(ind)
            if new_segment != []:
                free[row].append(new_segment)
            free[row].sort(key=lambda x: (x[0], x[1]))

        print(row + 1, l, r)
    else:
        print(-1)