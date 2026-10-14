#include<bits/stdc++.h>
using namespace std;
long long n,i,j,k,l,cnt=0,cnt1=0,sum=0,a;
string st;

int main()
{
    cin>>st;
    l=st.size();
    for(i=0;i<l;i++)
    {
        n=st[i]-'0';
        n=n%3;
        sum+=n;
        cnt1++;
        if(n==0||sum%3==0||cnt1==3)cnt++,cnt1=0,sum=0;
    }
    cout<<cnt<<endl;
}