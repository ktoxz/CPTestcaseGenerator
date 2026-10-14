from collections import defaultdict
import math

def pug_func(k: int, l: int) -> str:

    # arr = list(map(int, s.split(" ")))
    # rev_arr = arr[::-1]

    # s = set()
    # L = 0
    # for i in range(len(arr)):
    #     if rev_arr[i] not in s:
    #         s.add(rev_arr[i])
    #     else:
    #         break

    #     L += 1

    # return len(arr) - L

    if math.log(l) / math.log(k) == int(math.log(l) / math.log(k)):
        return "YES" + "\n" + str(int(math.log(l) / math.log(k))-1)
    
    else:
        return "NO"


k = int(input())
l = int(input())

x = pug_func(k, l)
print(x)


# t = int(input())
# lista_ans = []

# for _ in range(t):
#     n = input()
#     line = input()
#     lista_ans.append(line)

# for ans in lista_ans:
#     x = pug_func(ans)
#     print(x)