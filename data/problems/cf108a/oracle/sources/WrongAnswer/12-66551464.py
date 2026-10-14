time=input()
hh=int(time[0:2])
mm=int(time[3:])
a=hh%10*10+hh//10%10
if mm<a:
    print(time[0:2],":",time[1::-1],sep='')
else:
    h=str((hh+1)%24)
    if len(h)==1:
        h="0"+h
    print(h,":",h[1::-1],sep='')