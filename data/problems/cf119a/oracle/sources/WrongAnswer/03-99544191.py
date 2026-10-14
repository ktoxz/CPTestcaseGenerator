# def jewels(j, s):
#     count = 0
#     for i in j:
#         for stone in s:
#             if i == stone:
#                 count += 1
#     return count
#
# print(jewels("z", "ZZ"))

# # --- Even Number ---
# def even_num(x):
#     count = 0
#     for i in x:
#         if len(str(i)) % 2 == 0:
#             count += 1
#     return count
#
#
# nums = list(map(int, input().split(',')))
# print(even_num(nums))


# # --- Beautiful Year ---
# def beaut_year(year):
#     check = set(year)
#     while len(check) != 4:
#         year = str(int(year) + 1)
#         check = set(year)
#     return year
#
#
# a = str(int(input()) + 1)
# print(beaut_year(a))


# # --- Decompress Run-Length Encoded List ---
# # В новый список заносятся:
# # повторение второго элемента каждой пары в списке в кол-ве первого
# # из [1,2,3,4] получаем [2, 4, 4, 4] (2 повторяется 1 раз, а 4 три раза
# def enc_list(x):
#     new_list = []
#     for i in range(1, len(x), 2):
#         new_list += [x[i]] * x[i - 1]
#     return new_list
#
#
# a = list(map(int, (input()[1:-1]).split(',')))  # строка типа [1,2,3,4] преобразуется в список
# print(enc_list(a))


# # --- cAPS lOCK (internet) shit code ----
# s = input("")
#
#
# def chk(s, idx):
#     for i in range(idx, len(s)):
#         if s[i].islower():
#             return 0
#     return 1
#
#
# if chk(s, 0):
#     ns = s.lower()
# elif chk(s, 1):
#     ns = s[0].upper() + s[1:].lower()
# else:
#     ns = s
#
# print(ns)


# # --- cAPS lOCK (my solution)---
# def check(x):
#     if x[1:].isupper() and x[0].islower() or len(x) == 1 and x.islower():
#         return x.capitalize()
#     elif x.isupper():
#         return x.lower()
#     else:
#         return x
#
#
# a = input()
# print(check(a))


# --- Epic Game ---
def play_nod(sim, a_sim, st):
    num = [sim, a_sim]
    while st >= 0:
        for i in range(len(num)):
            if num[i] > st:
                if i == 0:
                    return 1
                else:
                    return 0
            c = num[i]
            rem = st
            while c > 0:
                rem, c = c, rem % c
            st = st - rem


a, b, n = map(int, input().split())
print(play_nod(a, b, n))

# print(play_nod(20, 5))