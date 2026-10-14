#include<bits/stdc++.h>
using namespace std;
int a[1010];
int b[1010];
int main(){
	int n,m;
	cin>>n>>m;
	long double ma=m;
	for(int i=0;i<n;i++)cin>>a[i];
	for(int i=0;i<n;i++)cin>>b[i];
	for(int i=0;i<n;i++)if(a[i]==1||b[i]==1)return cout<<-1,0;
	for(int i=n-1;i>=0;i--){
		ma=ma*b[(i+1)%n]/(b[(i+1)%n]-1);
		ma=ma*a[i]/(a[i]-1);
	}
	cout<<setprecision(7)<<fixed<<ma-m<<endl;
	return 0;
}