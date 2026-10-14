n, m, h = list(map(int, input().split()))
nums = list(map(int, input().split()))

def factorial(x):
    ans = 1
    while x:
        ans *= x
        x -=1
    return ans

def combination(x, r):
    ans = 0
    x_fac = factorial(x)
    r_fac = factorial(r)
    x_r_fac = factorial(x - r)
    ans = x_fac//(r_fac*x_r_fac)
    return ans  

total_player = sum(nums)
if total_player < n:
    print(-1)
    exit()
total_possiblity = combination(total_player - 1, n-1)
other_players= total_player - nums[h-1]
ans = 0
if other_players >= n:
    ans = combination(other_players, n - 1)    
# print(ans, total_possiblity )
print(1 - (ans/total_possiblity))