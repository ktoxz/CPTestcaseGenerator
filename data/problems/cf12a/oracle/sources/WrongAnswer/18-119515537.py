a = [input() for i in range(3)]
print("YES" if a[0]==a[2][::-1] and a[:][0]==a[:][2][::-1] else "NO")