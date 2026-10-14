f = open("input.txt", "r")
a = f.readline()
n = int(f.readline())

g = open("output.txt","w")
g.write('L' if n == 2 else 'R')