# Problem Link:         https://codeforces.com/problemset/problem/106/B
# Problem Status:
# ----------------------------------- SEPARATOR -----------------------------------
# IDEA:
#   Iterate over each laptop, whenever a laptop outdated found skip it, else add the laptop to a new array
#   Iterate over the new array, choose the cheapest one.
# ----------------------------------- SEPARATOR -----------------------------------
# Functions Definition:
def SolverA(Array):
    MinSpeed = 0
    MinRam = 0
    MinHDD = 0
    MinCost = 0
    Answer = 0
    NOD = []
    for E in range(len(Array)):
        X = Array[E]
        if X[0] > MinSpeed and X[1] > MinRam and X[2] > MinHDD:
            NOD.clear()
            X.append(E+1)
            NOD.append(X)
            MinSpeed = X[0]
            MinRam = X[1]
            MinHDD = X[2]
        elif X[0] < MinSpeed and X[1] < MinRam and X[2] < MinHDD:
            continue
        else:
            X.append(E+1)
            NOD.append(X)
    MinCost = NOD[0][3]
    for Y in NOD:
        if Y[3] < MinCost:
            MinCost = Y[3]
            Answer = Y[4]
    return Answer


# ----------------------------------- SEPARATOR -----------------------------------
# Scanning Input:
N = int(input())
A = []
for i in range(N):
    A.append([])
    Reader = input().split()
    for j in range(4):
        A[i].append(int(Reader[j]))
print(SolverA(A))
# ----------------------------------- SEPARATOR -----------------------------------