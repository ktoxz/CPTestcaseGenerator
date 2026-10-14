from math import ceil
p=int(input())
total_wgt=int(input());r1=total_wgt
lift=list(map(int,input().split()))
land=list(map(int,input().split()));n=len(land);ans=1e20
lift+=[lift[0]];land+=[land[0]]
l=0;r=1e20
while l<=r:
  mid=(l+r)/2
  c=0;a=mid
  for i in range(n):
    mid-=(total_wgt+mid)/lift[i]
    mid-=(total_wgt+mid)/land[i+1]
   # print(burn)
#  print(a,l,r)
  if mid>=0:ans=min(a,ans);r=a-1
  else:l=a+1
if ans< 1e20:
    print('%.17f' % ans)
else:
    print(-1)