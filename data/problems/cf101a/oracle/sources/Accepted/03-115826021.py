s = input()
k = int(input())
n = len(s)

c = {}

for x in set(s) : c[x] = s.count(x)

dp = sorted(set(s), key = lambda x : c[x])

while dp and c[dp[0]] <= k:
    k -= c[dp[0]]
    s = s.replace(dp[0],"")
    dp = dp[1:]
    
print(len(set(s)))
print(s)