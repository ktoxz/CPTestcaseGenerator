h, m = [int(x) for x in input().split(":")]
if h == 23:
    if m < 32:
        print("23:32")
    else:
        print("00:00")

elif h == 22:
    if m >= 55:
        print("23:32")
    else:
        m = m + 1
        while m % 11 != 0:
            m += 1
        print("22:" + str(m))

elif h == 21:
    if m < 12:
        print("21:12")
    else:
        print("22:00")
 
elif h == 20:
    if m < 2:
        print("20:02")
    else:
        print("21:12")
 
elif h == 19 or h == 18 or h == 17 or h == 16:
    print("20:02")
 
elif h == 15:
    if m < 51:
        print("15:51")
    else:
        print("20:02")
 
elif h == 14:
    if m < 41:
        print("14:41")
    else:
        print("15:51")
 
elif h == 13:
    if m < 31:
        print("13:31")
    else:
        print("14:41")
 
elif h == 12:
    if m < 21:
        print("12:21")
    else:
        print("13:31")
 
elif h == 11:
    if m >= 55:
        print("12:21")
    else:
        m = m + 1
        while m % 11 != 0:
            m += 1
        print("11:" + str(m))

elif h == 10:
    if m < 1:
        print("10:01")
    else:
        print("11:00")
 
elif h == 9 or h == 8 or h == 7 or h == 6:
    print("10:01")
 
elif h == 5:
    if m < 50:
        print("05:50")
    else:
        print("10:01")
 
elif h == 4:
    if m < 40:
        print("04:40")
    else:
        print("05:50")
 
elif h == 3:
    if m < 30:
        print("03:30")
    else:
        print("04:40")

elif h == 1:
    if m < 10:
        print("01:10")
    else:
        print("02:20")
 
elif h == 2:
    if m < 20:
        print("02:20")
    else:
        print("03:30")

else:
    if m >= 55:
        print("01:10")
    else:
        m = m + 1
        while m % 11 != 0:
            m += 1
        print("00:" + str(m))