def swap(c, i, j):
    c = list(c)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)

def correct_solution(m, n):
    d = {}
    for i in range (10):
        d[i] = 0
    for i in range (len(m)):
        d[int(m[i])] += 1
    value = ""
    for i in range(10):
        value += str(i) * d[i]
    for i in range (len (value)):
        if (ord('0') != ord(value[i])):
            value = swap(value, i, 0)
            break
    if (int(value) == int(n)):
        return True
    return False

if __name__ == '__main__':
    m = input()
    n = input()
    # 0000111
    #print(correct_solution(m, n))
    if (correct_solution(m, n)):
        print("OK")
    else:
        print("WRONG_ANSWER")