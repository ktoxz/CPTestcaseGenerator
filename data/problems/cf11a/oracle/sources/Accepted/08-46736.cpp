#include <cstdio>
int n,m;
long long int x,t,p,AC;

int main(){
	scanf("%d%I64d",&n,&m);
	p=AC=0;
	for (int i=0;i<n;i++){
		scanf("%I64d",&x);
		if (p>=x){
			t=(p-x+m)/m;
			AC+=t;
			p=x+t*m;
		}
		else p=x;
	}
	printf("%I64d\n",AC);
	return 0;
}