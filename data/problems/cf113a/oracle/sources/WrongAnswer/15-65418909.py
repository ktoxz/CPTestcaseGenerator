s = input()

l_adj = ['lions', 'liala']
l_noun = ['etr', 'etra']
l_verb = ['initis', 'inites']

index_adj_mas = []
index_noun_mas= []
index_verb_mas = []
index_adj_fem = []
index_noun_fem = []
index_verb_fem = []

mas = []
fem = []

word = []

temp_index = 0

for i in range(len(s)):
    
    if s[i]==" ":
        word.append(s[temp_index:i])
        temp_index = i+1
    elif i == len(s)-1:
        word.append(s[temp_index:i+1])
        
#print(word)

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

print(index_adj_mas,
index_noun_mas,
index_verb_mas,
index_adj_fem,
index_noun_fem,
index_verb_fem)
'''

flag = 0

if ((len(mas)!=0 and len(fem)==0) or (len(fem)!=0 and len(mas)==0)) and (len(index_noun_fem)==1 or len(index_noun_mas)==1):
    print("Yes")
    
    if len(fem)!=0:
        for i in index_adj_fem:
            if index_noun_fem <= i:
                flag = 1 #false/no
                break
        for i in index_verb_fem:
            if index_noun_fem >= i:
                flag = 1 #false/no
                break
                
    elif len(mas)!=0:
        for i in index_adj_mas:
            if index_noun_mas <= i:
                flag = 1 #false/no
                break
        for i in index_verb_mas:
            if index_noun_mas >= i:
                flag = 1 #false/no
                break
elif ((len(mas)!=0 and len(fem)!=0) or (len(mas)==0 and len(fem)==0)) and (len(index_noun_fem)!=1 or len(index_noun_mas)!=1):
    flag = 1
    
if flag==0:
    print("YES")
else:
    print("NO")