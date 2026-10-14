n = int(input())

# card values
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'jacks', 'queens', 'kings', 'aces']

# boolean indicating whether to count aces as 1 or 11 
count_aces_as_11 = False

# number of ways to reach n
ans = 0

# loop through each of the 14 card values
for value in values:
    # if value is jacks, queens, kings, aces
    if type(value) == str:
        # add 10 to ans 
        ans += 1
    # if value is aces
    elif value == 'aces':
        if count_aces_as_11:
            # add 11 to ans
            ans += 1
        else:
            # add 1 to ans
            ans += 1
    # if value is less than 10
    elif value < 10:
        # if n is at least 10
        if n - 10 >= 0:
            # add 1 to ans
            ans += 1
    # else, value is number >= 10
    else:
        # if n is at least value
        if n - value >= 0:
            # add 1 to ans
            ans += 1

# print answer
print(ans)