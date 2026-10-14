#include<iostream>
#include<stdio.h>
#include<queue>
#include<stack>
#include<algorithm>
#include<cmath>

using namespace std;

int main()
{
    long long k, l, m, i=0;
    cin>>k>>l;
    m = k;
    while(m<l)
    {
        m *= k;
        i++;
    }
    if(m==l)
        cout<<"YES"<<endl<<i;
    else
        cout<<"NO";

    return 0;
}