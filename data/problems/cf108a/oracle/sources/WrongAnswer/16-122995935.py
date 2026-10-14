a,b=map(int,input().split(':'))
if a+1==24:print('00:00')
else:print(str(a+1)+':'+str(a+1)[::-1])