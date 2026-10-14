#include <iostream>

#include <cstdio>

#include <string>

#include <cmath>

#include <vector>

#include <queue>

#include <map>

#include <cstring>

#include <algorithm>

using namespace std;



typedef long long ll;



#define ss(a) scanf("%s",a)

#define si(a) scanf("%d",&a)

#define sii(a,b) scanf("%d %d",&a,&b)

#define siii(a,b,c) scanf("%d %d %d",&a,&b,&c)

#define sll(a) scanf("%I64d",&a)

#define pi(a) printf("%d\n",a)

#define op(a) printf("%d ",a)

#define ps(a) printf("%s\n",a)

#define ppi(a,b) printf("%d %d\n",a,b)

#define pll(a) printf("%I64d\n",a)

#define all(c) c.begin(), c.end()

#define F first

#define S second

#define nl printf("\n");

#define pb push_back

#define mp make_pair

#define f(i,a,b) for(int i=a;i<b;i++)

#define MOD 1000000007

#define fastscan ios_base::sync_with_stdio(0); cin.tie(NULL);

//------------------MAIN CODE BEGINS-------------------

int main()

{

	fastscan;

	int n;

	cin>>n;

	n-=10;

	if(n<=0 || n>11){

        cout<<0;

        return 0;

	}

    int ans=0;

    if(n==10)

        ans=15;

    else

        ans=4;

    cout<<ans;

    return 0;

}