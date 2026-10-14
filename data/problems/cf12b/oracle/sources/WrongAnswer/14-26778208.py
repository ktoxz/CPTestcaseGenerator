def Ordenar(N):
    Ordenado = ''
    A = [0]*10
    for k in N:
        for i in range (0,10):
            if int(k)==i:
                A[i] += 1
    Aux = 0
    for k in range (1,10):
        if A[k]!=0:
            Aux = k
            break
    Ordenado = str(Aux)
    for j in range (A[0]):
        Ordenado += str(0)
    for k in range (Aux+1,10):
        if A[k]!=0:
            for i in range(A[k]):
                Ordenado += str(k)
    return Ordenado
A = input()
B = input()
Ord = Ordenar(A)
if Ord == B:
    print('OK')
else:
    print('WRONG_ANSWER')