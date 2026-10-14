#include <iostream>
#include <algorithm>
#include <map>
using namespace std;
long long n,m[300000],m2[300000],k,i,j,sum,h,z;
map <int,int>m1;
main(){
	cin>>n;
	h=n;
	for (i=0; i<n; i++){
		cin>>m2[i]; m1[m2[i]]++;
	}
	for (i=2; i<=2000000000; i*=2){
		m[j]=i; j++;
	}
	k=j;
	for (i=0; i<n; i++) {
		for (j=0; j<k; j++){
			if ( (m1[m[j]-m2[i]]>=1 && m[j]!=m2[i]*2) || (m1[m[j]-m2[i]]>=2) ) {
				z++; break;
			}
		}
		if(z==1) h-=1; z=0;
	}
	cout<<h;
}