#include <stdio.h>
#include <string.h>
#include <vector>
using namespace std;

#define N 105
vector<int> edgs[105];

int n, m, vis[N], p[N];
void init(int n){ for(int i=1; i<=n; ++i) p[i]=i, edgs[i].clear(); }
int find(int x) { if(p[x]!=x) p[x]=find(p[x]); return p[x]; }
void uni(int x, int y) { if(find(x)!=find(y)) p[x]=find(y); }

int stack[N];
int tail;
int loopn=0;
void dfs(int x, int pa) {
  vis[x]=1;
  stack[tail++]=x;
  for(int i=0;i<edgs[x].size();++i) 
    if(edgs[x][i]!=pa) {
      int y=find(edgs[x][i]);
      if(vis[y]==1) {
		loopn ++;
        int t=tail;
        while(find(stack[t-1])!=y) uni(stack[--t], y);
      }
      else if(vis[y]==0) dfs(y, x);
    }
  vis[x]=2;
  --tail;
}

int main() {
	int n, m;
	scanf("%d%d", &n, &m);
	init(n);
	for(int i=0; i<m; ++i) {
		int a, b;
		scanf("%d%d", &a, &b);		
		edgs[a].push_back(b);
		edgs[b].push_back(a);
	}
	dfs(1,-1);
	for(int i=1;i<=n;++i)
		if(vis[i]==0) {
			puts("NO");
			return 0;
		}
	if(loopn != 2) {		
		puts("NO");
		return 0;
	}
	puts("FHTAGN!");
	return 0;
}