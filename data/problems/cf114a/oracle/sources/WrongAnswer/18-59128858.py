from math import log

Base = int(input())
Symbol = int(input())
if "{0:.8f}".format(log(Symbol, Base)) == "{0:.8f}".format(int(log(Symbol, Base))):
    print("YES", int(log(Symbol, Base)) - 1, sep='\n')
else:
    print("NO")

# UB_CodeForces
# Advice: Be on your own
# Location: Based on popular demand "" "" "" ""
# Caption: Last breath
# CodeNumber: 574