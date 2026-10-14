import sys
sys.stdin = open('input.txt', 'r')
sys.stdout = open('output.txt', 'w')
print("R" if input()=="back" else "L")