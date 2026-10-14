#include <stdio.h>
#include <math.h>
#define ld long double
int A[2222];
int n,m;
ld dp(ld w, int i){
	if(i<0) return w;
	ld b = (w/A[i])/(1-(1/(ld)A[i]));
	return dp(b+w, i-1);
}
int main(){
	scanf("%i%i",&n,&m);
	int i;
	for(i=0;i<2*n;i+=2)
		scanf("%i", &A[i]);
	for(i=1;i<2*n;i+=2)
		scanf("%i", &A[i]);
	ld ans=dp(m, i-2)-m;
	printf("%.8Lf\n", isnormal(ans)?ans:-1);
}