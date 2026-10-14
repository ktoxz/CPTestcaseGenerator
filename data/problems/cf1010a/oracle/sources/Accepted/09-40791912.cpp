#include<bits/stdc++.h>
double now;
int n,k,i,cnt;
int main(){
	scanf("%d %d",&cnt,&n);
	now=n;
	for(i=0;i<cnt*2;i++){
		int t;
		scanf("%d",&t);
		if(t==1){
			return !printf("-1");
		}
		now*=(double)t/(t-1);
	}
	printf("%lf",now-n);
}