#include<stdio.h>

int a[128][2];
int n;

int main() {
	int ret=0,i,j,p1,p2,p3,t1,t2;

	scanf("%d %d %d %d %d %d",&n,&p1,&p2,&p3,&t1,&t2);
	for(i=0;i<n;i++) scanf("%d %d",&a[i][0],&a[i][1]);
	for(i=a[0][0],j=0;i<a[n-1][1];i++) {
		if (i<a[j][1]) ret+=p1;
		else if (i>=a[j+1][0]) j++, ret+=p1;
		else if (i-a[j][1]>=t1+t2) ret+=p3;
		else if (i-a[j][1]>=t1) ret+=p2;
		else ret+=p1;
	}
	printf("%d\n",ret);
	return 0;
}