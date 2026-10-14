def find_str(a):
    count = a.count('AB')
    a = a.replace('AB','')
    count *= a.count('BA')
    return "YES" if count else "NO"

a = input()
print(find_str(a))