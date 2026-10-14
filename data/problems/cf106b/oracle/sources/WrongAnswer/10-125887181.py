import sys
msg = "".join(sys.stdin.readlines())
ls = [i.split() for i in str(msg[1:]).splitlines()]
print(ls.index(max(ls[1:])))