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

def Lucky_Sum_of_Digits2():
    n = inp()

    possible_b = []
    possible_a = []
    num_of_digits = []

    b = 1
    while True:
        a_num = (n - (7*b))/4

        if a_num < 0 :
            break

        if a_num == int(a_num):
            possible_b.append(b)
            possible_a.append(int(a_num))
            num_of_digits.append(int(a_num) + b)
        
        b += 1 
    
    if len(possible_a) == 0:
        print(-1)
        return 
     
    min_digits = min(num_of_digits)
    final_a = min_digits
    final_b = min_digits

    for index,digits_count in enumerate(num_of_digits):

        if digits_count == min_digits:
            
            if possible_b[index] < final_b:
                final_b = possible_b[index]
                final_a = possible_a[index]
    
    outputStr = ('4'*final_a) + ('7'*final_b)
    print(outputStr)
    return 

Lucky_Sum_of_Digits2()