#include <vector>
#include <list>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include<string.h>
using namespace std;
#define ff(i,a,b)  for(int i=a;i<=b;i++)
#define fil(x,y) memset(x,y,sizeof(x))
#define fre1     freopen("Untitled2.cpp","r",stdin)
#define fre2     freopen("out.txt","w",stdout)
#define max_int 999999999
#define LLmax_int 999999999999999999LL
typedef long long bigint;
typedef pair<int,int> Pair;
typedef vector<int> Vector;
#define pi acos(-1*1.0)     
//3.141592653
#define exp  1e-8  
#define ma 102
#define lowbit(x) (x&(-x))
#define Lson(L,R)  L,(L+R)>>1,i*2
#define Rson(L,R)  ((L+R)>>1)+1,R,i*2+1
#define Mid   (L+R)>>1
#define Ls(x)    x*2
#define Rs(x)    x*2+1
int n;
bigint num[ma];
bigint num2[ma];
int main(){
    while(cin>>n){
     ff(i,1,n)
     {
      cin>>num[i];
      num2[i]=num[i]-1;
     }
     bigint ans=0;
     ff(i,1,n){
     
        ans+=num[i];
       for(int j=i+1;j<=n;j++)
       {
        ans+=num2[j];
       }
      // cout<<ans<<" "; 
     
     }
      cout<<ans<<endl;
    //cout<<endl;  
    }
  
}