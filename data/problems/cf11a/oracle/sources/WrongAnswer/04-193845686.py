def lastindex(arr:int, n:int) -> int:
    for i in range(1,n+1):
        if arr[-i]==n:
            index=-i
            break
    return index

def solve():
    n,k=list(map(int,input().split( )))
    arr=list(map(int,input().split( )))
    max=0
    max
    for i in arr:
        if i>=max:
            max=i
    check=False
    move=0
    i=0
    if n==2:
        if arr[0]>=arr[1]:
            (arr[0],arr[1])=(arr[1],arr[0])
            move = move + 1
        print(move)
        return
    while i<(n-1):
        if arr[i]>arr[i+1]:
            (arr[i],arr[i+1])=(arr[i+1],arr[i])
            move = move + 1
            if (n-3) - (i) > 3:
                for j in range(i,n-2):
                    if arr[j] < (arr[j+1] + k) and (arr[j+1] + k) < arr[j+2]:
                        check=True
                        arr[j+1] = arr[j+1] + k
                        break
                    else:
                        check=False
            if check==False:
                arr[lastindex(arr,max)] = arr[lastindex(arr,max)] + k
                max = max + k
            i=0
            print(arr)
        else:
            i=i+1
    print(move)
solve()