#include<cassert>
#include<cstring>
#include<cstdio>
#include<vector>
#include<string>
#include<set>
#include<map>
#include<cmath>
#include<iostream>
#include<algorithm>
#define eps 1e-12
#define sqr(a) (a)*(a)
#define forn(i,n) for(int i=0;i<(int)n;i++)
#define taskname ""
typedef long long ll;
using namespace std;
int main()         
{
  #ifdef DEBUG
  freopen(taskname".in","r",stdin);                         
  freopen(taskname".out","w",stdout);
  #endif
  int n;
  cin>>n;
  int ans=1;
  n=abs(n);
  while(true)
  {
    cerr<<n<<endl;
    if(n<=0&&n%2==0)
    {         
      printf("%d\n",ans-1);
      return 0;
    }
    n-=ans;
    ans++;
  }
  return 0;
}