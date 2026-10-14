#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <cmath>
#include <cstring>
#include <queue>
#include <list>

using namespace std;

#define foreach(i,n) for(__typeof(n.begin()) i=n.begin();i!=n.end();i++)
#define REP(i,n) for(int i = 0; i < (n); i++)
#define FOR(i,a,b) for(int i = (a); i <= (b); i++)
#define RFOR(i,a,b) for(int i = (a); i >= (b); i--)
#define SIZE(x) ((int)(x).size())
#define LENGTH(x) ((int)(x).length())
#define PB push_back

template<typename T> inline void checkmin(T &a, T b) {if(a>b) a=b;}

bool dfs(int &tap,int &dia,int tank,int N,int n,
    int rounte[],int dorm[],int visited[],int depth = 0)
{
    if(depth == 0) {
        memset(visited,0x00,sizeof(int)*n);
        visited[tank] = 1;
        dia = 10000000;
    }
    else {
        if(visited[tank]) return false;
        visited[tank] = 1;
        // cerr << tank << endl;
    }

    for(int i = 0; i < n; i++) {
        int tmp = rounte[tank*N+i];
        if(tmp > 0) {
            if(dia > tmp) dia = tmp;
            if(dorm[i] < 0) {
                tap = i;
                return true;
            }
            return dfs(tap,dia,i,N,n,rounte,dorm,visited,depth+1);
        }
    }

    return false;
}

const int N = 1000;
int dorm[N];
int visited[N];
int rounte[N*N];

void solve()
{
    memset(rounte,0x00,sizeof(rounte));
    memset(dorm,0x00,sizeof(dorm));
    int n,p;
    scanf("%d%d",&n,&p);
    for(int i = 0; i < p; i++) {
        int a,b,d;
        scanf("%d%d%d",&a,&b,&d);
        a--;b--;
        dorm[a]++;dorm[b]--;
        rounte[a*N+b] = d;
    }

    // cerr << "ok" << endl;

    vector<int> all;
    for(int i = 0; i < n; i++) {
        if(dorm[i] > 0) {
            int tap,dia;
            bool res = dfs(tap,dia,i,N,n,rounte,dorm,visited);
            if(res) {
                all.push_back(i);
                all.push_back(tap);
                all.push_back(dia);
            }
        }
    }

    int t = all.size();
    printf("%d\n",t/3);
    for(int i = 0; i < t; i+=3) {
        printf("%d %d %d\n",all[i]+1,all[i+1]+1,all[i+2]);
    }
}

int main()
{
	solve();
	return 0;
}