chars = input()
num = int(input())
count_dict = {}
delete_list = []
solved_order = '-'.join(chars).split('-')
char_list = sorted(solved_order)
seted_char_list = set(char_list)
if len(char_list) < num:
    print(0)
    print('\n')
else:
    for seted_char in seted_char_list:
        count_dict.setdefault(char_list.count(seted_char),[]).append(seted_char)
    
    # print(count_dict)  
    seted_list = []
    for key in count_dict.keys():
        if key == 1:
            for single in count_dict.get(key):
                seted_list.append(single)
        else:
            num_1 = 0
            while num_1+key<=len(count_dict.get(key))*key:
                seted_list.append(sorted(count_dict.get(key)*key)[num_1:num_1+key])
                num_1+=key

    # print(seted_list)
    for i in seted_list:
        num = num - len(i)
        if num >= 0:
            delete_list.append(i)   
    
    for i in delete_list:
        if type(i) != str:
            for j in i:
                solved_order.remove(j)
        else:
            solved_order.remove(i)
    # print(delete_list)
    print(len(set(solved_order)))
    for word in solved_order:
        print(word,end='')