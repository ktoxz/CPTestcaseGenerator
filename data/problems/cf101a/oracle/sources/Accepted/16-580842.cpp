/*
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <queue>
#include <stack>
#include <algorithm>
#include <cstring>
#include <map>
#define B 100
#define oo 1000000000
#define pf printf
#define sf scanf
#define mp make_pair
#define pb push_back
#define FORL(i,b) for(int i=0,l=v[b].size();i<l;i++)
#define FOR(i,a,b) for(int i=a;i<b;i++)
#define FORB(i,a,b) for(int i=a-1;i>=b;i--)
#define FORC(i,a,b,c) for(int i=a;i<b;i+=c)
#define rst(arr,x) memset(arr,x,sizeof(arr))
using namespace std;

int n,m,a[B][B]={0},p[B]={0};

int main(){
    int x,y,pmin=-1,act;
    sf("%d%d",&n,&m);
    FOR(i,0,n)sf("%d",&p[i]);
    FOR(i,0,m){
        sf("%d%d",&x,&y);
        x--;y--;
        a[x][y]=a[y][x]=1;
    }
    FOR(i,0,n)FOR(j,i+1,n)FOR(k,j+1,n){
        if(a[i][j]&&a[i][k]&&a[j][k]){
            act=p[i]+p[j]+p[k];
            if(act<pmin||pmin==-1)pmin=act;
        }
    }
    pf("%d",pmin);
}
*/




/*
#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <vector>
#include <queue>
#include <stack>
#include <algorithm>
#include <cstring>
#include <string>
#include <map>
#define B 100
#define oo 1000000000
#define pf printf
#define sf scanf
#define mp make_pair
#define pb push_back
#define FORL(i,b) for(int i=0,l=v[b].size();i<l;i++)
#define FOR(i,a,b) for(int i=a;i<b;i++)
#define FORB(i,a,b) for(int i=a-1;i>=b;i--)
#define FORC(i,a,b,c) for(int i=a;i<b;i+=c)
#define rst(arr,x) memset(arr,x,sizeof(arr))
using namespace std;

int dale(int x){
    int s=0;
    if(x>=100000)s+=(x/100000)%10;
    if(x>=10000)s+=(x/10000)%10;
    if(x>=1000)s+=(x/1000)%10;
    if(x>=100)s+=(x/100)%10;
    if(x>=10)s+=(x/10)%10;
    s+=x%10;
    return s;
}

int main(){
    string n;
    int sum=0,cant=1;
    cin>>n;
    if(n.size()==1){
        pf("0");
        return 0;
    }
    FOR(i,0,n.size()){
        sum+=n[i]-'0';
    }
    while(sum>9){
//        pf(" %d",sum);
        sum=dale(sum);
//        pf(" %d\n",sum);
        cant++;
    }
    pf("%d",cant);
}
*/




#include <cstdio>
#include <cstdlib>
#include <vector>
#include <queue>
#include <iostream>
#include <stack>
#include <algorithm>
#include <cstring>
#include <map>
#define B 26
#define oo 1000000000
#define pf printf
#define sf scanf
#define mp make_pair
#define pb push_back
#define FORL(i,b) for(int i=0,l=v[b].size();i<l;i++)
#define FOR(i,a,b) for(int i=a;i<b;i++)
#define FORB(i,a,b) for(int i=a-1;i>=b;i--)
#define FORC(i,a,b,c) for(int i=a;i<b;i+=c)
#define rst(arr,x) memset(arr,x,sizeof(arr))
using namespace std;

string n;
int k;

struct let{int x,cant;}c[B];

bool cmp(let a,let b){return a.cant<b.cant;}
bool cmp1(let a,let b){return a.x<b.x;}

int main(){
    int cmin=oo,act;
    FOR(i,0,B)c[i].x=i;
    cin>>n;
    sf("%d",&k);
    int st=n.size();
    FOR(i,0,st)c[n[i]-'a'].cant++;
    sort(c,c+B,cmp);
    int i;
    for(i=0;i<B;i++){
        if(c[i].cant>k)break;
        k-=c[i].cant;
        c[i].cant=0;
    }
    pf("%d\n",B-i);
    sort(c,c+B,cmp1);
    FOR(i,0,st){
        if(c[n[i]-'a'].cant>0){
            pf("%c",n[i]);
            c[n[i]-'a'].cant--;
        }
    }
//    while(1);
}