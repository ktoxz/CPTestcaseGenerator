def div3(s, index_0, index_1):
    c = 0
    for i in range(index_0, index_1+1):
        c += int(s[i])
        c = c%3
    if c == 0:
        return True
    return False


s = input()
strings_list = [s]
d = 0
c = 0
while True:
    next_string_list = []
    for string in strings_list:
        i = 0
        keep = 0
        to_keep = []
        while i < len(string)-d:
            if div3(string, i, i+d):
                c += 1
                if i != keep:
                    to_keep.append((keep, i-1))
                i += d+1
                keep = i
            else:
                i += 1
        if keep != i:
            to_keep.append((keep, len(string)-1))

        for keeping in to_keep:
            next_string_list.append(string[keeping[0]:keeping[1]+1])
    strings_list = next_string_list[:]
    
    d += 1

    for string in strings_list:
        if len(string) > d:
            break
    else:
        break


print(c)

# Fri Oct 01 2021 22:56:12 GMT+0300 (Москва, стандартное время)