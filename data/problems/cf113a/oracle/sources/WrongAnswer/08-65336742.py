def find_str(a):
    temp = a
    
    count = a.count('AB')
    a = a.replace('AB','',1)
    count *= a.count('BA')
    
    if count:
        return "YES" if count else "NO"
    else:
        count = temp.count('BA')
        temp = temp.replace('BA','',1)
        count *= temp.count('AB')
        return "YES" if count else "NO"

a = input()
print(find_str(a))