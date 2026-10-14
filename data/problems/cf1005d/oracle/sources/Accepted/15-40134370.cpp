#include <iostream>
#include<bits/stdc++.h>
using namespace std;
string s;
long long ans;
set<long long>mod;
int main()
{
cin>>s;
long long mod3=0;
for(int i=0;i<s.size();i++)
{
    mod3+=s[i]-'0';
    if(mod3%3==0)
    {
        mod3=0;
        ans++;
        mod.clear();
    }
    else
    {
        if(mod.count(mod3%3))
        {
            mod3=0;
            ans++;
            mod.clear();
        }
        else
            mod.insert(mod3%3);
    }
}
cout<<ans;
    return 0;
}