#include <iostream>
using namespace std;
int main(){
	int n;
	string a,b;
	cin>>n>>a>>b;
	int ans=0;
	for(int i=0;i<n/2;i++){
		int j=n-i-1;
		if((a[i]==a[j]&&b[i]==b[j])||(a[i]==b[i]&&a[j]==b[j])||(a[i]==b[j]&&a[j]==b[i])){
			
		}else
		if(b[i]==b[j]||a[i]==b[i]||a[i]==b[j]||(a[j]==b[i]||a[j]==b[j])){
			ans++;
		}else ans+=2;
	}
	if(n%2==1){
		if(a[n/2]!=b[n/2])ans++;
	}
	cout<<ans;
}