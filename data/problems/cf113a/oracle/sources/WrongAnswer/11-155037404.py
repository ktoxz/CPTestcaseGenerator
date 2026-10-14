def isPetyaLanguage():
    str_lst = input().split(" ")
    lst = list(map(basic_test, str_lst))
    if len(lst) == 1:
        if 0 not in lst:
            print("YES")
        else:
            print("NO")
    elif lst.count(0) != 0:
        print("NO")
    elif lst.count(3)+lst.count(4) != 1:
        print("NO")
    elif (lst[0] in (1, 3)) and (3 in lst):
        if((2 or 4) in lst[0:lst.index(3)]) or ((5 or 6) in lst[0:lst.index(3)]):
            print("NO")
        elif((1 or 2) in lst[lst.index(3)::]) or ((5 or 6) in lst[lst.index(3)::]):
            print("NO")
        else:
            print("YES")
    elif (lst[0] in (2, 4)) and (4 in lst):
        if((1 or 3) in lst[0:lst.index(4)]) or (5 or 6) in lst[0:lst.index(4)]:
            print("NO")
        elif((2 or 3) in lst[lst.index(4)::]) or ((5 or 6) in lst[lst.index(4)::]):
            print("NO")
        else:
            print("YES")
    else:
        print("NO")
    return


def basic_test(test_str):
    if test_str[-4::] == "lios":
        return 1
    elif test_str[-5::] == "liala":
        return 2
    elif test_str[-3::] == "etr":
        return 3
    elif test_str[-4::] == "etra":
        return 4
    elif test_str[-6::] == "initis":
        return 5
    elif test_str[-6::] == "inites":
        return 6
    return 0

if __name__ == "__main__":
    isPetyaLanguage()