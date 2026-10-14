n, k = map(int, input().split())
a = list(map(int, input().split()))

free = [[[1, k]] for i in range(k)]

order = []
for i in range(k // 2, -1, -1): order.append(i)
for i in range(k // 2 + 1, k): order.append(i)

for i in range(n):
    found = False
    take_middle = False
    row, l, r = 0, 0, 0
    need_place = a[i]
    distance = 10 ** 10
    ind = 0
    new_segment = []

    for j in order:
        if free[j] == [[]]:
            continue
        for place in free[j]:
            left = place[0]
            right = place[1]

            if right - left + 1 >= need_place:
                found = True

                if left == 1 and right == k:
                    take_middle = True
                    row, l, r = j, k // 2 + 1 - need_place // 2, k // 2 + 1 + (need_place - 1) // 2
                    if need_place == k:
                        free[j] = [[]]
                    elif need_place == k - 1:
                        free[j] = [[k, k]]
                    else:
                        free[j] = [[1, l - 1], [r + 1, k]]
                    break

                else:
                    if right < k // 2:
                        new_distance = k // 2 - right
                        if new_distance < distance:
                            distance = new_distance
                            row, l, r = j, right - need_place + 1, right
                            ind = free[j].index(place)
                            if right - left + 1 > need_place:
                                new_segment = [1, left - 1]

                    else:
                        new_distance = left - k // 2
                        if new_distance < distance:
                            distance = new_distance
                            row, l, r = j, left, left + need_place - 1
                            ind = free[j].index(place)
                            if right - left + 1 > need_place:
                                new_segment = [right + 1, k]

            if found:
                break
        if found:
            break

    if found:
        if take_middle:
            pass
        else:
            free[row].pop()
            if new_segment != []:
                free[row].append(new_segment)
            free[row].sort(key=lambda x: (x[0], x[1]))

        print(row + 1, l, r)
    else:
        print(-1)