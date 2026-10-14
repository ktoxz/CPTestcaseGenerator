def check_completion(fuel):
    weight = m + fuel
    for i in range(n):
        take_off_fuel = weight / a[i]
        weight -= take_off_fuel
        if weight <= m:
            return False
        landing_fuel = weight / b[i]
        weight -= landing_fuel
        if weight < m:
            return False


    return True

        

n = int(input())
m = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

left = 0
right = 10 ** 9

while right - left > (1e-6):
    mid = (left + right) / 2
    if check_completion(mid) == True:
        right = mid
    else:
        left = mid

if check_completion(mid) == True:
    print(round(mid, 6))
else:
    print("-1")