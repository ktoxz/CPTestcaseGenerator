import sys 
input = sys.stdin.buffer.readline 

def process(n, A):
    S = 0 
    L = []
    for i in range(1, n+1):
        s1 = i*(i-1)//2 
        s2 = (n-i)*(n+1-i)//2 
        L.append(s1+s2)
    L = [min(L), max(L)]
    for x, d in A:
        entry = -1*float('inf')
        for op in L:
            entry =max(entry, n*x+d*op)
        S+=entry 
        print(x, d, entry)
    answer = S/n 
    sys.stdout.write(f'{answer}\n')
                
n, m = [int(x) for x in input().split()]
A = []
for i in range(m):
    x, d = [int(x) for x in input().split()]
    A.append([x, d])
process(n, A)