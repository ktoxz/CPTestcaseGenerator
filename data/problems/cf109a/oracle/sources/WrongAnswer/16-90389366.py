def lucky_no (n):
    ans = ""
    dup = n
    if n%7 == 0 :
        return "7" * (n//7)
    else:
        i = n//7
        while i >= 0:
            dup = n
            dup -= (i*7)
            if dup%4 == 0:
                ans += "4" * (dup//4) + "7"
                ans += "7" * i
                return ans
            else:
                i -= 1
        return -1
            

print (lucky_no(int(input())))