import sys
import math

#to read string
get_string = lambda: sys.stdin.readline().strip()
#to read list of integers
get_int_list = lambda: list( map(int,sys.stdin.readline().strip().split()) )
#to read integers
get_int = lambda: int(sys.stdin.readline())
#to print fast
pt = lambda x: sys.stdout.write(str(x)+'\n')

#--------------------------------WhiteHat010--------------------------------------#
with open('input.txt','r') as f:
    gate = f.readline()
    rail = f.readline()
    if gate == 'front':
        if rail == '1':
            res = 'L'
        else:
            res = 'R'
    else:
        if rail == '1':
            res = 'R'
        else:
            res = 'L'
with open('output.txt','w') as g:
    g.writelines(res)