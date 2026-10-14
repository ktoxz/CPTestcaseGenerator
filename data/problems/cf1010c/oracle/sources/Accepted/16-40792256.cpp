#include <bits/stdc++.h>
using namespace std;
int main(){
	int n,k;
	scanf("%d%d",&n,&k);
	int g=k;
	for(int i=1;i<=n;i++){
		int x;
		scanf("%d",&x);
		x%=k;
		g=__gcd(g,x);
	}
	printf("%d\n",k/g);
	for(int i=0;i<k/g;i++){
		printf("%d ",i*g);
	}
}