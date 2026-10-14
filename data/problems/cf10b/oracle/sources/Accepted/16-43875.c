#include<stdio.h>
#include<stdlib.h>

int a[128][128];
int n,m;

int main() {
	int i,j,p,x,y,t,ans,s,mid;
	for(scanf("%d %d",&n,&m),mid=m/2;n--;) {
		scanf("%d",&p);
		ans=1000000000,x=y=-1;
		for(i=0;i<m;i++) {
			for(s=t=j=0;j<m;j++) {
				if (a[i][j]) t=s=0; else s++,t+=abs(j-mid);
				if (s>=p) {
					if (t+abs(i-mid)*p<ans) ans=t+abs(i-mid)*p,x=i,y=j;
				}
				if (s>=p) t-=abs(j-p+1-mid);
			}
		}
		if (x==-1) puts("-1"); else {
			for(j=0;j<p;j++) a[x][y-j]=1;
			printf("%d %d %d\n",x+1,y-p+2,y+1);
		}
	}
	return 0;
}