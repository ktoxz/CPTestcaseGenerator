import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input()
    return(list(s[:len(s) - 1]))
def invr():
    return(map(int,input().split()))
############ ---- Input Functions ---- ############

def Blackjack():
    n = inp()
    possiblePoints = [x for x in range(1,12)]
    possiblePoints.remove(10)

    remainingPoints = n - 10

    if remainingPoints in possiblePoints:
        print(4)
    elif remainingPoints == 10:
        print(15)
    else:
        print(0)
    return 

Blackjack()