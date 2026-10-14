#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<math.h>

char a[48][32];
int v[48];
int n,m,k;
int idx[48];

int cmp(const void *t1,const void *t2) {
	return strcmp(a[*(int *)t1],a[*(int *)t2]);
}

int main() {
	int i,j;
	double p;
	scanf("%d %d %lf",&n,&m,&p);
	k=(int)floor(p*100+1e-12);
	for(i=0;i<n;i++) {
		scanf("%s %d",a[i],&v[i]);
		v[i]=v[i]*k/100;
		if (v[i]<100) i--,n--;
	}
	for(i=0;i<m;i++) {
		scanf("%s",a[i+n]);
		for(j=0;j<n;j++) if (strcmp(a[j],a[i+n])==0) break;
		if (j<n) i--,m--; else v[i+n]=0;
	}
	n+=m;
	for(i=0;i<n;i++) idx[i]=i;
	qsort(idx,n,sizeof(idx[0]),cmp);
	printf("%d\n",n);
	for(i=0;i<n;i++) printf("%s %d\n",a[idx[i]],v[idx[i]]);
	return 0;
}