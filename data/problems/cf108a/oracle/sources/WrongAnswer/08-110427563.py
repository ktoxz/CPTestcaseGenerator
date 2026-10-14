try:
    def pali(a):
        f=a%10
        g=a//10
        z=f*10+g
        return z
        
    a,b=map(int,input().split(':'))
    e=pali(b)
    if(a==23 and b>=32):
        print("00:00")
    else:
        while(e>=60):
            a=a+1
            e=pali(a)
        if(a<10):
            integer=str(a)
            a=integer.zfill(2)
        if(e<10):
            integer=str(e)
            e=integer.zfill(2)
        print(a,e,sep=':')    
        
        


except:
    pass