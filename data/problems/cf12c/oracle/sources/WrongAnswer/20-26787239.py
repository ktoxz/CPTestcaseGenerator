def Invertir(A):
    B =[]
    k = len(A)-1
    while k>=0:
        B.append(A[k])
        k -=1
    return B
def SinRepetir(A):
    ASP = [0]
    for k in range (len(A)):
        if k==0:
            ASP[0]=A[k]
        c = 0
        for i in range (len(ASP)):
            if A[k]==ASP[i]:
                c+=1
        if c==0:
            ASP.append(A[k])
    return ASP    
L = input()
L = L.split()
n = int(L[0])
m = int(L[1])
P = input()
P = P.split()
Frutas = []
for k in range (len(P)):
    P[k] = int(P[k])
for k in range (m):
    F = str(input())
    Frutas.append(F)
FrutasSinRepetir = SinRepetir(Frutas)
Contador = [0]*len(FrutasSinRepetir)
for k in range (len(FrutasSinRepetir)):
    for i in range (len(Frutas)):
        if Frutas[i]==FrutasSinRepetir[k]:
            Contador[k] += 1
P.sort()
CInv = Invertir(Contador)
Menor = 0
Mayor = 0
for k in range (len(CInv)):
    Menor += CInv[k]*P[k]
j = len(P)-1
i = len(Contador)-1
while i>=0:
    Mayor += P[j]*Contador[i]
    j -= 1
    i -=1
print(Menor, Mayor)