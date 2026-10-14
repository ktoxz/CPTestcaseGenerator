#include <stdio.h>
#include <string.h>

int smallest[1000];
int len[1000];

char ans[1000000];
char cur[1000000];

int bestlen;

int INF=1000000000;

void putcur(int num,int at) {
  for(--at;at>=0;at--) cur[at]=num%10+48,num/=10;
}

int main() {
  int i,j,k,tall,digsum,a,cand,candlen;
  memset(smallest,127,sizeof(smallest));
  memset(len,127,sizeof(len));
  smallest[0]=0;
  len[0]=0;
  for(i=1;i<9;i++) {
    for(j=0;j<(1<<i);j++) {
      tall=0;
      digsum=0;
      for(k=0;k<i;k++) {
        if(j&(1<<k)) tall=tall*10+7, digsum+=7;
        else tall=tall*10+4,digsum+=4;
      }
      if(smallest[digsum]>tall) smallest[digsum]=tall,len[digsum]=i;
    }
  }
again:
  if(scanf("%d",&a)!=1) return 0;
  cand=a/7;
  bestlen=INF;
  while(cand>=0) {
    i=a-cand*7;
    if(i>200) break;
    if(smallest[i]<INF) {
      candlen=cand+len[i];
      if(candlen<bestlen) {
        bestlen=candlen;
        putcur(smallest[i],len[i]);
        for(j=len[i];j<1000;j++) cur[j]='9';
        memcpy(ans,cur,1000);
      } else if(candlen==bestlen) {
        putcur(smallest[i],len[i]);
        for(j=len[i];j<1000;j++) cur[j]='9';
        for(j=0;j<1000;j++) {
          if(cur[j]<ans[j]) goto good;
          if(cur[j]>ans[j]) goto bad;
        }
        goto bad;
      good:
        memcpy(ans,cur,1000);
      bad:;
      }
    }
    cand--;
  }
  if(bestlen>=INF) puts("-1");
  else {
    for(j=0;cur[j]<'9';j++) putchar(cur[j]);
    for(;j<bestlen;j++) putchar('7');
    putchar('\n');
  }
  goto again;
  return 0;
}