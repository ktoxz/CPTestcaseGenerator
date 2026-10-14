s = input()

digits = [int(d) for d in str(s)]
digits.sort(reverse=True)  # Sort the digits in descending order for easy removal

ans = 0

# Step 1: Calculate the sum of the digits
digit_sum = sum(digits)

# Step 2: If the sum is divisible by 3, return the number of cuts made plus 1
if digit_sum % 3 == 0:
    print(len(digits) - 1 + 1)
    exit(0)

# Step 3: Remove digits to make the sum divisible by 3
remove_count = 0  # Number of digits removed
while remove_count < len(digits):
    removed = False

    # Step 3a: Find the minimum number of digits that leave a remainder of 1 or 2 when divided by 3
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] % 3 == 1:
            digits.pop(i)
            removed = True
            break
        elif digits[i] % 3 == 2:
            digits.pop(i)
            removed = True
            break

    if not removed:
        break  # No more digits can be removed

    remove_count += 1

    # Step 3d: Recalculate the sum of the remaining digits
    digit_sum = sum(digits)

    # Step 2: If the sum is divisible by 3, return the number of cuts made plus 1
    if digit_sum % 3 == 0:
        ans = len(digits) - 1 + 1

print(ans)