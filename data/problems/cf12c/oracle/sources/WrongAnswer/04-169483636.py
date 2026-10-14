from collections import Counter

n , m = map(int,input().split())

l = sorted(map(int,input().split()))

print(sum(l[:len(Counter(l))]), sum(l[-len(Counter(l)):]))