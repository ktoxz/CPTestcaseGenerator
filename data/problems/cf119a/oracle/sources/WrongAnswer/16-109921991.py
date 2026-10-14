def separator(s, a):
    output_list = []
    inter = ""
    for ind, i in enumerate(s):
        if i != a:
            inter += i
            if ind == len(s) - 1:
                output_list.append(int(inter))
        else:
            if inter:
                output_list.append(int(inter))
                inter = ""
    return output_list


def find_sides_recur(l):
    if l[0] + l[1] <= l[len(l) - 1]:
        return f'1 2 {len(l)}'
    return "-1"


def joiner(l, a):
    output_str = ""
    for loc, i in enumerate(l):
        if not loc == len(l) - 1:
            output_str += i + a
    output_str += l[len(l) - 1]
    return output_str


def euclidean_thorem(a, b):
    if a == b:
        return a
    elif a < b:
        return euclidean_thorem(b, a)
    elif b == 0:
        return a
    else:
        return euclidean_thorem(b, a % b)


def game_recursion(a, b, n):
    turn = 0
    def helper(a, b, n, turn):
        if not turn % 2 and n < euclidean_thorem(a,n):
            return "1"
        elif turn % 2 and n < euclidean_thorem(b,n):
            return "0"
        else:
            if turn % 2:
                return helper(a, b, n - euclidean_thorem(n,a), turn + 1)
            else:
                return helper(a, b, n - euclidean_thorem(n, b), turn + 1)
    return helper(a, b, n, turn)






def main_func():
    a = input()
    lisa = []
    a, b, n = separator(a, " ")
    return game_recursion(a, b, n)


print(main_func())