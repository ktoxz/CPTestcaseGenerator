TS_ADD = input().split()
sequence = input().split()
sortcounter = 0
intsequence = [int(_) for _ in sequence]
addsequence = [int(_) for _ in TS_ADD]
def sortthisthing(number):
    sortcounter = 0
    n = len(number)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if number[j] > number[j+1]:
                number[j], number[j+1] = number[j+1], number[j]
                swapped = True
                sortcounter += 1
        if not swapped:
            break
    return(sortcounter)
print(sortthisthing(intsequence)+1)