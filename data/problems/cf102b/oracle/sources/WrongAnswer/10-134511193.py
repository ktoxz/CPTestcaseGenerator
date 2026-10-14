def f(n):
    if n<10:
        return 0
    return 1+f(n%10+n//10)

print(f(int(input())))