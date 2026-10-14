#include<iostream>
#include<fstream>
using namespace std;

int main() {
long long n, a[111], i, j, k=0, l=0;
cin>>n;
for (i=1; i<=n; i++){
cin>>a[i];
}
for (i=1; i<n; i++){
k+=(a[i]-1)*i;
}
k+=a[n]*n;
cout<<k;
return 0;
}