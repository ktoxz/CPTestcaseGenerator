def main_function():
    s = list(input())
    still_there = [False for i in range(len(s))]
    k = int(input())
    hash_n = {}
    for i in s:
        if i in hash_n:
            hash_n[i] += 1
        else:
            hash_n[i] = 1
    another_hash = {}
    listy_2 = [[]]
    current_ind = 0
    for i in range(len(s)):
        if s[i] in another_hash:
            index = another_hash[s[i]]
            listy_2[index].append(i)
        else:
            another_hash[s[i]] = current_ind
            listy_2.append([])
            index = another_hash[s[i]]
            listy_2[index].append(i)
            current_ind += 1
   # print(listy_2)
    listy = [[i, hash_n[i]] for i in hash_n]
    listy.sort(reverse=True)
    for i in range(len(listy)):
        if k > 0:
            if k >= listy[i][1]:
                k -= listy[i][1]
                listy[i][1] = 0
            else:
                break
    counter = 0
    listy_3 = []
    for i in listy:
        if i[1] > 0:
            counter += 1
            target_letter = i[0]
            ind = another_hash[target_letter]
            for j in listy_2[ind]:
                listy_3.append([target_letter, j])
    listy_3.sort(key=lambda x:x[1])
    print(counter)
    for i in range(len(listy_3)):
        if i == len(listy_3) - 1:
            print(listy_3[i][0])
        else:
            print(listy_3[i][0], end="")






if __name__ == '__main__':
    main_function()