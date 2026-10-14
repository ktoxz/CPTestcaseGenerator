def nik(rud):
    rud=abs(rud)
    t=0
    x=0
    while(x<rud or (x-rud)%2!=0):
        t+=1
        x+=t
    print(t)
rud=int(input())
nik(rud)