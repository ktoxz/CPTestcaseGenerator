#include<bits/stdc++.h>

using namespace std;

long long n,m,k;

int main(){

long long n;

cin>>n;

long long ans=0;

for(int i=0;i<n;i++){

    long long x;cin>>x;

    ans+=(i*(x-1));

    ans+=(x);

}cout<<ans<<endl;

return 0;}