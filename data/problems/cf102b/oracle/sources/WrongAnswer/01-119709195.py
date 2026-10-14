n = input()
c = 0
while n > '9':
    n = str((n.count('9') * 9) + (n.count('8') * 8) + (n.count('7') * 7) + (n.count('6') * 6) + (n.count('5') * 5) + (n.count('4') * 4) + (n.count('3') * 3) + (n.count('2') * 2) + n.count('1'))
    c += 1
print(c)