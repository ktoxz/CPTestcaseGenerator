#include <iostream>
using namespace std;
int main()
{
    __int64 a,b,i=0;
    cin>>a>>b;
    __int64 c=a;
while(a<b)
{
    a*=c;
    i++;
}
if(a==b)
{
    cout<<"YES"<<endl;
    cout<<i;
    return 0;
}
else 
{
    cout<<"NO";
    return 0;
}
}