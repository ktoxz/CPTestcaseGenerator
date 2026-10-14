#n, k = map(int, input().split(" "))        # read multiple integers into different variables
#L = [int(x) for x in input().split()]      # read multiple integers into a list
#print(' '.join(map(str, L)))               # print multiple integers in one line

n = int(input())

ct = 0
for i in range(4) :
    for j in range(1, 14) :
        if ((i != 0) or (j != 12)) :
            if (j == 1) :
                if ((10 + 1 == n) or (10 + 11 == n)) : ct += 1
            elif (j >= 10) and (10 + 10 == n) : ct += 1
            elif (10 + j == n) : ct += 1

print(ct)