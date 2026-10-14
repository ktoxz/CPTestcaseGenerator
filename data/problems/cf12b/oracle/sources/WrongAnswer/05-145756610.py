# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# |AUTHOR|
# |      |
# |      |
# |      |
# |      | 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MUHAMMAD AMMAR
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
A=input();B=input()
Input=list(map(int,list(A)))
Input2=list(map(int,list(B)))
List=[]
Min_Current=min(Input)
if len(A)!=len(B):
    print('WRONG_ANSWER')
elif Input.count(0)==0:
    Ml=Input2.copy()
    Ml.sort()
    an=''
    for m in Ml:
        an+=str(m)
    if B==an:
        print('OK')
    else:
        print('WRONG_ANSWER')
else:
    Count_of_zero=Input.count(0)
    for i in Input:
        if i!=0:
            List.append(i)
    Str=''
    for Li in range(len(List)):
        Str+=str(min(List))
        List.remove(min(List))
    FinalSTR=Str[0]+(Count_of_zero*'0')+Str[1:]
    X=Input.copy()
    X.sort()
    ans=0
    Y=[]
    for j in range(len(X)):
        if X[j]!=0:
            Y.append(X[j])
        else:
            ans+=1
    fin=''
    fin+=str(Y[0])+(ans*'0')
    for m in range(1,len(Y)):
        fin+=str(Y[m])
        
    if fin==B:
        print('OK')
    else:
        print('WRONG_ANSWER')