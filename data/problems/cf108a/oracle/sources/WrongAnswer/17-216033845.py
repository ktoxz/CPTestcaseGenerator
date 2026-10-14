hh, mm = (int(i) for i in input().split(":"))
if mm >= int(str(hh)[::-1]):
    hh = hh + 1 if hh < 23 else 0
hh = f"{hh:02d}"
res = f"{hh}:{hh[::-1]}"
print(res)