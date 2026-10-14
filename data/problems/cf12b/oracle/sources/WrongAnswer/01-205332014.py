n1 = input()
n2 = int(input())
nb_zero = n1.count("0")
s = str(int("".join(sorted(n1))))
s = s[0] + nb_zero * "0" + s[1: ]
if int(s) < n2  : 
    print ("WRONG_ANSWER")
else :
    print("OK")