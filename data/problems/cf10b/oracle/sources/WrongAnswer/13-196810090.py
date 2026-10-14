n,k = map(int, input().split())
a = [ int(i) for i in input().split()]
mid = (k+1) // 2
taken = [[k,k] for i in range(k)] 
for i in range(n):
    flag = False
    best = [k ** 3, k, k]
    for j in range(k):
        if taken[j][0] == taken[j][1]:
            x = j + 1
            left = mid - a[i] // 2
            score = abs(mid - j - 1) * a[i]
            if a[i] % 2 == 0:
                score += ((1 + a[i] // 2) * a[i] // 2 - a[i] // 2)
            else:
                score += (1 + a[i] // 2) * a[i] // 2
            if score < best[0] or ( score == best[0] and (x < best[1] or (x == best[1] and left < best[2]) )):
                best[0] = score
                best[1] = x
                best[2] = left
                flag = True
        else:
            x = j + 1
            if taken[j][0] >= a[i]:
                left = taken[j][0] - a[i] + 1
                score = abs(mid - j - 1) * a[i] 
                score += (left + a[i] -1)*a[i] // 2
                if score < best[0] or ( score == best[0] and (x < best[1] or (x == best[1] and left < best[2]) )):
                    best[0] = score
                    best[1] = x
                    best[2] = left
                    flag = True
            if taken[j][1] + a[i] - 1 <= k:
                left = taken[j][1]
                score = abs(mid - j - 1) * a[i] 
                score += (left + a[i] -1)*a[i] // 2
                if score < best[0] or ( score == best[0] and (x < best[1] or (x == best[1] and left < best[2]) )):
                    best[0] = score
                    best[1] = x
                    best[2] = left
                    flag = True
    if flag :
        #print(best)
        print(best[1], best[2], best[2] + a[i] - 1)
        if taken[best[1] - 1][0] == taken[best[1] - 1][1]:
            taken[best[1]-1][0] = left - 1
            taken[best[1]-1][1] = left + a[i]
        else:
            if left < taken[best[1]-1][0]:
                taken[best[1]-1][0] = left - 1
            else:
                taken[best[1]-1][1] = left + a[i]
    else:
        print(-1)
    #print(taken)