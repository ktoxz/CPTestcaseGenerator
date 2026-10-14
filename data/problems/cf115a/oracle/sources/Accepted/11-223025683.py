# # # to get min num divisable by n and > l --> ceil(l/i)*i
# # # to get min num divisable by n and > l --> ceil(l/i)*i
# # # from queue import PriorityQueue
# # import math 
# # # from math import gcd
# # # from functools import reduce
# # # def find_gcd(list):
# # #     x = reduce(gcd, list)
# # #     return x
# # # a = []


# # # for KK in range(int(input())):

# # #     n = int(input())
# # #     l = list(map(int,input().split()))
# # #     if n == 1 :
# # #         a.append(0)
# # #     else :
# # #         dic = {}
# # #         for i in l :
# # #             dic[i] = dic.get(i,0)+1 
# # #         ll = []
# # #         s = list(set(l))
# # #         r = len(s)
# # #         for i in range(r):
# # #             for j in range(i):
# # #                 for  k in range(min(dic[s[i]],dic[s[j]])) :
# # #                     ll.append(s[i]+s[j])
        
        
# # #         for k , v in dic.items() :
# # #             lll = [k*2]*(v//2)
# # #             ll += lll

# # #         dict2 = {}
# # #         for i in ll :
# # #             dict2[i] = dict2.get(i,0)+1

# # #         a.append(max(dict2.values()))
# # # for i in a :
# # #     print(i)
    

# # # import numpy
# # # print(numpy.bitwise_xor.reduce([1,1,1,1,1]))
# # # def valid(i,j):
# # #     if i in range(3) and j in range(3):
# # #         return True 
# # #     else :
# # #         return False 

# # # n , m = map(int,input().split())
# # # l = []
# # # for i in range(n):
# # #     l.append(list(map(str,input().split())))
# # # dic = {}
# # # for i in range(3):
# # #     for j in range(3):
# # #         dic[(i,j)] = False
# # # def fib(l,i,j): 
    
# # #     if not valid(i,j) or l[i][j] == "X" or dic[(i,j)] == True :
# # #         return 
    
# # #     ll.append(1)
# # #     dic[(i,j)] = True 
# # #     fib(l,i+1,j)
# # #     fib(l,i-1,j)
# # #     fib(l,i,j+1)
# # #     fib(l,i,j-1)
    
    
# # # ll = []
# # # fib(l,0,0)
# # # print(len(ll))



# # # def generatebinary(len, cur=""):
# # #     if len == 0 :
# # #         print(cur)
# # #         return 
# # #     else :
# # #         generatebinary(len-1,cur+"0")
# # #         generatebinary(len-1,cur+"1")
# # #         generatebinary(len-1,cur+"2")


# # # generatebinary(3)

# # # def ks(W,weight,value,size):
# # #     if W == 0 or size == 0 :
# # #         return 0
# # #     if weight[size-1] > W :
# # #         return ks(W,weight,value,size-1)
# # #     else :
# # #         return max(value[size-1]+ks(W-weight[size-1],weight,value,size-1),ks(W,weight,value,size-1))
# # # weight = []
# # # value = []

# # # n,m = map(int,input().split())
# # # for i in range(n):
# # #     a , b = map(int,input().split())
# # #     weight.append(a)
# # #     value.append(b)


# # # print(ks(m,weight,value,n))




# # # def find(i,l,lenn,a):
# # #     if lenn == len(l):
# # #         a.append(i)
# # #     else :
# # #         find(i+l[lenn],l,lenn+1,a)
# # #         find(i-l[lenn],l,lenn+1,a)

# # # a = []
# # # n , m = map(int,input().split())
# # # l = list(map(int,input().split()))
# # # find(l[0],l,1,a)
# # # if m in a:
# # #     print("YES")
# # # else :
# # #     print("NO")
              


# # # def rev(l,i,a):
# # #     if i == len(l) :
# # #         return 
# # #     else :
# # #         rev(l,i+1,a)
# # #         a.append(l[i])

# # # a = []
# # # n = int(input())
# # # l = list(map(int,input().split()))
# # # rev(l,0,a)
# # # if a == l :
# # #     print("YES")
# # # else :
# # #     print("NO")

# # # ll = []
# # # def find(i,l,MAX):
# # #     if i == 0 :
# # #         MAX = l[0]
# # #     if i == len(l):
# # #         return 
# # #     else :
# # #         if l[i] > MAX:
# # #             MAX = l[i]
# # #         print(MAX,end = " ")
# # #         return find(i+1,l,MAX)

# # # def calc(l1,l2,n,m,l):
# # #     if n == 0 :
# # #         return 
# # #     else :
# # #         if m == 0 :
# # #             l.reverse()
# # #             print(*l)
# # #             l = []
# # #         else :
# # #             l.append(l1[n-1][m-1]+l2[n-1][m-1])
# # #             calc(l1,l2,n,m-1,l)
# # #         calc(l1,l2,n-1,0,l)
    
# # # n , m = map(int,input().split())
# # # l1 = []
# # # l2 = []
# # # l = []
# # # for i in range(n):
# # #     l1.append(list(map(int,input().split())))
# # # for i in range(n):
# # #     l2.append(list(map(int,input().split())))

# # # calc(l1,l2,n,m,l)
# # # booked = []
# # # def delete(l,k,el):
# # #     if el in booked :
# # #         return sum(el)
# # #     else :
# # #         booked.append(el)
# # #         if k == 0 : return 0
# # #         else :
# # #             return min(l[-1] + delete(l[:-1],k-1,[l[-1]])
# # #                        , l[0]+l[1] + delete(l[2:],k-1, [l[0],l[1]]))
    
# # # l = [15, 22, 12, 10, 13, 11]
# # # l.sort()
# # # print(delete(l,2,[-1]))
# # # def binary(lista , el , bottom , top):
# # #     if bottom <= top :
# # #         middle = (top + bottom)//2
# # #         if lista[middle] == el :
# # #             return middle
# # #         elif lista[middle] > el and el > lista[middle-1] :
# # #             return middle-1 
# # #         elif lista[middle] < el and el < lista[middle+1] :
# # #             return middle
# # #         elif el < lista[middle] :
# # #             return binary(lista,el,bottom,middle-1)
# # #         else :
# # #             return binary(lista,el,middle+1,top)
# # #     return -1
# # # aa = []
# # # n = int(input())
# # # l = list(map(int,input().split()))
# # # ma = max(l)
# # # mi = min(l)
# # # l.sort()
# # # q = int(input())
# # # if len(set(l)) == 1 :
# # #     for i in range(q):
# # #         x = int(input())
# # #         if x >= l[0]:
# # #             aa.append(n)
# # #         else :
# # #             aa.append(0)
# # # else :
# # #     dic = {}
# # #     for i in range(q):
# # #         x = int(input())
# # #         if x in dic.keys():
# # #             aa.append(dic[x])
# # #         else :
# # #             if x >=ma :
# # #                 aa.append(n)
# # #                 dic[x] = n 
# # #             elif x < mi :
# # #                 aa.append(0)
# # #                 dic[x] = 0
# # #             else :
# # #                 id = binary(l,x,0,n-1) #3
# # #                 c = binary(l,x,0,n-1)+1
# # #                 for i in range(id+1,n):
# # #                     if l[i] == l[id] :
# # #                         c+=1 
# # #                     else :
# # #                         break
# # #                 aa.append(c)
# # #                 dic[x] = c



# # # for i in aa :
# # #     print(i)
# # import math 
# # a = []
# # for i in range(int(input())):
# #     n = int(input())
# #     if n == 1 or n == 3:
# #         a.append(["N"]) 
# #     elif n == 0 :
# #         a.append(["Y",0.0,0.0]) 
# #     elif n == 4 :
# #         a.append(["Y",2.0,0.0]) 


# #     else :
# #         l = n-1.5 
# #         r = 1.5
# #         try :
# #             while True :
# #                 if abs(n -l*r) < .01:
# #                     break 

# #                 elif l*r > n:
# #                     l = l/2 + math.floor(l)-math.floor(l/2)
# #                     if l < math.floor(l)+.5 :
# #                         l+=.5
# #                     r = n - l 
# #                 else : 
# #                     add = (abs(l-int(l)-.5))/2
# #                     l = l - add 
# #                     r = n - l
                    
# #             a.append(["Y",l,r])
# #         except:
# #             a.append(["N"]) 
# # for i in a :
# #     print(*i)
# # def calc(i,x,n,s,c):
# #     if s == x :
# #         c.append(1) 
# #         return 
# #     elif i**n > x :
# #         return
# #     if s > x :
# #         return 
# #     else :
# #         calc(i+1,x,n,s+i**n,c)
# #         calc(i+1,x,n,s,c)


# # c = []
# # calc(1,1000,10,0,c)
# # print(len(c)) 


# # def find(i,n,l,f):
# #     f.sort()
# #     if i == n+1 :
# #         return 
# #     else :
# #         if i in f :
# #             l.append("O")
# #         else :
# #             l.append("o")

# #         if i in f :
# #             f[0] = f[0]+f[1]
# #         find(i+1,n,l,f)

# # def find(i,n,x,y,l,dic):
# #     if i>n:
# #         return
# #     else :
# #         d = dic.get(i,0)
# #         if d == 0 :
# #             l.append(1)
# #             dic[i]=1
# #         find(i*10+x,n,x,y,l,dic)
# #         find(i*10+y,n,x,y,l,dic)
            

            
        
# # l = []
# # def find(n,s,l,o,c):
# #     if len(s) == n*2 :
# #         if o == c :
# #             l.append("".join(s))
# #         return 
# #     else :
# #         if o >=c :
# #             find(n,s+"(",l,o+1,c)
# #             find(n,s+")",l,o,c+1)

# # find(10,"",l,0,0)
# # print(l)

 
# # def func(i,l,s,ll):
# #     if sum(l) - s == s :
# #         ll.append("YES")
# #         return 
# #     elif i == 4 :
# #         return 
# #     else :
# #         func(i+1,l,s+l[i],ll)
# #         func(i+1,l,s,ll)

# # def f(i,n,m,l):
# #     if l :return 
# #     elif n == m :
# #         l.append(i)  
# #         return 
# #     elif n > m : 
# #         return
# #     else :
# #         f(i+1,n*2,m,l)
# #         f(i+1,n*3,m,l)
# # import math
# # n,m = map(int,input().split())
# # print(math.factorial(min(n,m)))

# # def f(i,s,sum,l,value,ll):
# #     if i == len(s):
# #         ll.append(1)
# #         if sum == value :
# #             l.append(1)
# #             return
# #     else :
# #         if s[i] == "+":
# #             f(i+1,s,sum+1,l,value,ll)
# #         elif s[i] == "-":
# #             f(i+1,s,sum-1,l,value,ll)
# #         else :
# #             f(i+1,s,sum+1,l,value,ll)
# #             f(i+1,s,sum-1,l,value,ll)

# # s1 = input()
# # s2 = input()
# # value = s1.count("+") - s1.count("-")
# # l = []
# # ll = []
# # f(0,s2,0,l,value,ll)
# # print((len(l))/len(ll))

# #      __IMPORTANT__ 
# #      Make tree and get depth
# # def f(original_l,l,ll,d):
# #     if l == []:
# #         return 
# #     else :
# #         i = original_l.index(max(l))
# #         ll[i] = d 
# #         j = l.index(max(l))
# #         f(original_l,l[:j],ll,d+1)
# #         f(original_l,l[j+1:],ll,d+1)


# # def f(i,ll,l):
# #     cl = []
# #     if i == 1 :
# #         return
# #     for j in range(len(l)-1):
# #         cl.append(l[j]+l[j+1])
# #     cl = [1] + cl + [1]
# #     ll.append(cl)
# #     f(i-1,ll,cl)
# # l = [[1]]



# # from collections import Counter
# # n = int(input())
# # l = (list(map(int,input().split())))
# # c = 0
# # dic = Counter(l)

     
    
# # print(dic.most_common(1))

# aa = []
# def f(l,s,c,i,n,ll,op):
#     if i == n :
#         ll.append(c)
#         return 
#     if s[i] == "1":
#         if i == 0 or op :
#             f(l,s,c+l[i],i+1,n,ll,True)
#         else :
#             f(l,s,c+l[i],i+1,n,ll,True)
#             f(l,s,c+l[i-1],i+1,n,ll,False)
#     else :
#         f(l,s,c,i+1,n,ll,False)
# for _ in range(int(input())):
#    n = int(input())
#    s = input()
#    cur = s[0]
#    ss = ""
#    i = 1 
#    while i < n :
#        if s[i] == cur :
#            ss+=cur
#            try:
#               cur = s[i+1]
#            except :
#                pass
        
#            i+=2 
#        else :
#            i+=1
   




    
#    aa.append(ss)
# for i in aa :
#     print(i)

# def f(i,n,k,l,ll,c,lll):
#     if c <= n and c not in lll:
#         ll.append(1)
#         lll.append(c)
#     if i == len(l) :
#         return
#     f(i+1,n,k,l,ll,c+l[i],lll)
#     f(i+1,n,k,l,ll,c,lll)
# import math
# print(math.floor(9937214561053071/2))
# print(round(.5))
# 4943329752812629795
# x1,y1,x2,y2,x3,y3,x4,y4 = map(int,input().split())
# x = [x1,x2,x3,x4]
# y = [y1,y2,y3,y4]
# n = int(input())
# aa = []
# for i in range(n):
#     xx,yy = map(int,input().split())
#     if xx >= min(x) and xx<=max(x) and yy >=min(y)and yy<=max(y):
#         aa.append("YES")
#     else :
#         aa.append("NO")
# for i in aa :
#     print(i)

n = int(input())
graph = {}
m1a = []
aa = []
for i in range(n):
    graph[i+1] = [] 
for i in range(n):
    nn = int(input())
    if nn!=-1 :
        graph[nn].append(i+1)
    else :
        m1a.append(i+1)

for i in m1a :
    start = i
    vis = (n+1)*[0]
    level = (n+1)*[-1]
    vis[start] = 1 
    level[start] = 1 
    queue = [start]
    ans = []
    while queue :
        parent = queue[0]
        ans.append(parent)

        queue.remove(parent)
        for i in range(len(graph[parent])):
            child = graph[parent][i]
            if not vis[child]:
                vis[child] = 1 
                level[child] = level[parent]+1
                queue.append(child)

    aa.append(max(level))
print(max(aa))