def inp_spl(f): return map(f,input().split())
def inp(f): return map(f,input())
NMAX = 101

left = [None] * NMAX
right = [None] * NMAX
K = 1
mid = 1
N = 1

def initialize():
    global left
    global right
    global mid
    for i in range(NMAX):
        left[i] = K
        right[i] = K
    mid = K // 2 + 1

def find_space(size, row, side, flush): #side - 0 for left, 1 for right; flush - 0 for check, 1 for flush
    global left
    global right
    if(side == 1):
        if(right[row] >= size):
            if(right[row] == K):
                if(flush == 1):
                    print('{} {} {}'.format(row, mid - size // 2, mid + size // 2 - 1 + size % 2))
                    right[row] = (K - size) // 2 + (K - size) % 2
                    left[row] = right[row] - 1 + size % 2
                else:
                    return size * abs(row - mid) + (size // 2) * (size // 2 + 1) - ( size // 2 * ( (size % 2 + 1 ) % 2 ) )
            else:
                if(flush == 1):
                    print('{} {} {}'.format(row, K - right[row] + 1 , K - right[row] + size))
                    right[row] -= size
                else:
                    return size * abs(row - mid) + (mid - right[row] - 1) * size + size * (size + 1) // 2
    else:
        if(left[row] >= size):
            if(left[row] == K):
                if(flush == 1):
                    print('{} {} {}'.format(row, mid - size // 2, mid + size // 2 - 1 + size % 2))
                    right[row] = (K - size) // 2 + (K - size) % 2
                    left[row] = right[row] - 1 + size % 2
                else:
                    return size * abs(row - mid) + (size // 2) * (size // 2 + 1) - ( size // 2 * ( (size % 2 + 1 ) % 2 ) )
            else:
                if(flush == 1):
                    print('{} {} {}'.format(row, left[row] - size + 1 , left[row]))
                    left[row] -= size
                else:
                    return size * abs(row - mid) + (mid - left[row] - 1) * size + size * (size + 1) // 2
    if(flush == 0):
        return -1


def Main():
    global N
    global K
    N, K = inp_spl(int)
    initialize()
    for x in inp_spl(int):
        ud = -987
        lr = -987
        minResult = 100000
        for j in range(K // 2 + 1):
            sideResult = find_space(x, mid - j, 0, 0)
            if(sideResult != -1 and minResult > sideResult):
                minResult = sideResult
                ud = -j
                lr = 0
            sideResult = find_space(x, mid - j, 1, 0)
            if(sideResult != -1 and minResult > sideResult):
                minResult = sideResult
                ud = -j
                lr = 1
            sideResult = find_space(x, mid + j, 0, 0)
            if(sideResult != -1 and minResult > sideResult):
                minResult = sideResult
                ud = j
                lr = 0
            sideResult = find_space(x, mid + j, 1, 0)
            if(sideResult != -1 and minResult > sideResult):
                minResult = sideResult
                ud = j
                lr = 1
        if(ud == -987):
            print (-1)
        else:
            find_space(x, mid + ud, lr, 1)
        

    
Main()