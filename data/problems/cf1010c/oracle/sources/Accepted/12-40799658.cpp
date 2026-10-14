#include<bits/stdc++.h>
#include<cstdlib>   
#define sf(x) scanf("%d",&x)
#define pf(x) printf("%d ",x)
#define sf2(x,y) scanf("%d %d",&x,&y)
#define pf2(x,y) printf("%d %d ",x,y)
#define sf3(x,y,z) scanf("%d %d %d",&x,&y,&z)
#define pf3(x,y,z) printf("%d %d %d ",x,y,z)
#define sfc(c) scanf(" %c",&c)
#define pfc(c) printf("%c",c)
#define pb(x) push_back(x)
#define mp(x,y) make_pair(x,y)
#define INF 1000000008
#define ENDL puts("")


using namespace std;

typedef long long ll;
typedef unsigned long long ull;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
typedef unsigned int uint;
typedef long double ld;



set<int> res;
int a[100100];



int gcd(int a, int b)
{
    if(b==0) return a;
    return gcd(b,a%b);
}


int qwe[100100];


int main()
{
    /*
    freopen("test.in","r",stdin);
    freopen("test.out","w",stdout);
    /**/
    
    int n,k;
    sf2(n,k);
    for(int i=0; i<n; i++)
    {
        sf(a[i]);
        res.insert(gcd(a[i],k)%k);
    }
    for(auto i: res)
    {
        qwe[i]=1;
    }
    for(int j=0; j<10; j++)
    for(auto q: res)
    {
        for(int i=0; i<k; i++)
        {
            if(qwe[i])
            {
                qwe[(i+q)%k]=1;
            }
        }
    }
    int cnt=0;
    for(int i=0; i<k; i++)
    {
        cnt+=qwe[i];
    }
    printf("%d\n",cnt);
    for(int i=0; i<k; i++)
    {
        if(qwe[i])
        {
            printf("%d ",i);
        }
    }
    
    
    return 0;

}