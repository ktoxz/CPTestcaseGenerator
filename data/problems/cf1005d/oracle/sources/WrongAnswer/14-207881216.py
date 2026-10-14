nums = input()

res = 0
i = 0
while i < len(nums):
    if int(nums[i]) % 3 == 0:
        res += 1
        i += 1

    else:
        temp = int(nums[i])

        for j in range(i + 1, len(nums)):
            if int(nums[j]) % 3 == 0:
                res += 1
                i = j
                break
            else:
                temp += int(nums[j])
                if temp % 3 == 0:
                    i = j 
                    res += 1
                    break
        i += 1

print(res)