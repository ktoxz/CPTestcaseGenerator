#include <bits/stdc++.h>
using namespace std;

int main () {
	long long n,m,x,d;
	cin>>n>>m;
	long long maxn=n*(n-1)/2;
	long long minn=0;
	long long i=1;
	long long t=0,ans=0;
	while(1){
		if(n/2-i>=0)minn+=i;
		if(n/2+i<n)minn+=i;
		if(n/2-i<0||n/2+i>=n)break;
		i++;
	}
	// cout<<maxn << " " << minn<<'\n';
	while(m--){
		cin>>x>>d;
		ans+=x;
		t+=(d>0 ? maxn : minn)*d;
	}
	double answer=ans+(double)t/n;
	printf("%.7f\n",answer);
	return 0;
}