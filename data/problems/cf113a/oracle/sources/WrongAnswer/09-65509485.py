s = input()

l_adj = ['lios', 'liala']
l_noun = ['etr', 'etra']
l_verb = ['initis', 'inites']

word = []

temp_index = 0

for i in range(len(s)):
    
    if s[i]==" ":
        word.append(s[temp_index:i])
        temp_index = i+1
    elif i == len(s)-1:
        word.append(s[temp_index:i+1])
        

index_adj_mas = []
index_noun_mas= []
index_verb_mas = []
index_adj_fem = []
index_noun_fem = []
index_verb_fem = []

mas = []
fem = []

for i in range(len(word)):

    if word[i].endswith(l_noun[0]):
        mas.append(word[i])
        index_noun_mas.append(i)

    elif word[i].endswith(l_adj[0]):
        mas.append(word[i])
        index_adj_mas.append(i)

    elif word[i].endswith(l_verb[0]):
        mas.append(word[i])
        index_verb_mas.append(i)

    elif word[i].endswith(l_noun[1]):
        fem.append(word[i])
        index_noun_fem.append(i)

    elif word[i].endswith(l_adj[1]):
        fem.append(word[i])
        index_adj_fem.append(i)

    elif word[i].endswith(l_verb[1]):
        fem.append(word[i])
        index_verb_fem.append(i)

'''
print(mas , fem)
print(len(mas),len(fem),len(word))

print(index_adj_mas,
index_noun_mas,
index_verb_mas,
index_adj_fem,
index_noun_fem,
index_verb_fem)

'''
def f(word):
    
    flag = 0
    
    if len(word)==1:
        if len(index_adj_mas)+len(index_noun_mas)+len(index_verb_mas)+len(index_adj_fem)+len(index_noun_fem)+len(index_verb_fem) == 0:
            flag = 1
        else:
            flag = 0
            
    else:
        if (len(mas)==len(word) or len(fem)==len(word)) and (len(index_noun_fem)==1 or len(index_noun_mas)==1):
            #print("Yes")

            if len(fem)==len(word):
                if len(index_adj_fem)>0:
                    for i in range(len(index_adj_fem)):
                        if index_noun_fem[0] <= index_adj_fem[i]:
                            flag = 1 #false/no
                            #print("1")
                            break
                if len(index_verb_fem)>0:
                    for i in range(len(index_verb_fem)):
                        if index_noun_fem[0] >= index_verb_fem[i]:
                            flag = 1 #false/no
                            #print("2")
                            break

            elif len(mas)==len(word):
                if len(index_adj_mas)>0:
                    for i in range(len(index_adj_mas)):
                        if index_noun_mas[0] <= index_adj_mas[i]:
                            flag = 1 #false/no
                            #print("3")
                            break
                if len(index_verb_mas)>0:
                    for i in range(len(index_verb_mas)):
                        if index_noun_mas[0] >= index_verb_mas[i]:
                            flag = 1 #false/no
                            #print("4")
                            break
        elif (len(mas)!= len(word) or len(fem)!=len(word)) and (len(index_noun_fem)!=1 or len(index_noun_mas)!=1):
            flag = 1
            #print("5")
            
    return flag

        
#print(word)

result = f(word)
    
if result==0:
    print("YES")
else:
    print("NO")