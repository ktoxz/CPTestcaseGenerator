# import pandas as pd
# df = pd.read_csv("Iris.csv")
# # print(df)
# x = df.iloc[:,1:5].values
# y = df.iloc[:,5].values
# from sklearn.model_selection import train_test_split
# x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=
# 0)
# from sklearn.linear_model import LogisticRegression
# Log = LogisticRegression()
# Log.fit(x_train,y_train)
# y_pred = Log.predict(x_test)
# # Log.pred
# print(y_test)
# print(y_pred)
# from sklearn.metrics import accuracy_score,mean_absolute_error,confusion_matrix
# print(accuracy_score(y_test,y_pred))
# tot = int(input("How many tries you want to do.\nIf you want to stop enter n"))
# print(tot)
# while n:
#     b = input("Enter pred")
tot = int(input())
arr = []
for x in range(tot):
    lst = list(map(int,input().split(" ")))
    lst.append(x+1)
    arr.append(lst)
arr.sort(key = lambda x: x[0])
ot = 0
if tot==1:
    print(1)
else:
    for x in range(1,tot):
        fg = 0
        for y in range(4):
            if not arr[x][y]>arr[x-1][y]:
                fg = 0
                break
            else:
                fg = 1
        if fg:
            ot = x
# print("arr is")
# print(arr)
# print("ot =",ot)
c = arr[ot:]
c.sort(key= lambda x:x[3])
print(c[0][-1])