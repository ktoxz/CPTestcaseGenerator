def endsWith(s, f):
    if len(s) < len(f): return False
    else: return s[-len(f):] == f

def solve():
    words = input().split()
    
    if len(words) == 1: return True

    ans = []
    for i in range(len(words)):
        if endsWith(words[i], "lios"): ans.append(1)
        elif endsWith(words[i], "etr"): ans.append(2)
        elif endsWith(words[i], "initis"): ans.append(3)
        elif endsWith(words[i], "liala"): ans.append(4)
        elif endsWith(words[i], "etra"): ans.append(5)
        elif endsWith(words[i], "inites"): ans.append(6)
        else: return False
    
    
    m = words[i] in range(1, 4)
    for i in range(len(ans) - 1):
        if ans[i] > 3 and m: return False
        elif ans[i] <= 3 and not m: return False

        if i < len(ans) - 1 and ans[i] > ans[i + 1]: return False
    
    return m and ans.count(2) == 1 or not m and ans.count(5) == 1

print("YES" if solve() else "NO")