#include<bits/stdc++.h>

using namespace std;

int n,m;

vector<vector<int> >adj;

bool vis[105];

int cnt=0;

void dfs(int node,int par){

    if(vis[node])return;

    vis[node]=true;

    bool flag=0;

    for(auto v:adj[node]){

        if(!vis[v])dfs(v,node);

        else if(v!=par)cnt++;

    }

}

int ccc(){

    for(int i=1;i<=n;i++)

        if(!vis[i])return 0;

return 1;}

int main(){

scanf("%d%d",&n,&m);

adj.resize(n+1);

for(int i=0;i<m;i++){

    int x,y;scanf("%d%d",&x,&y);

    adj[x].push_back(y);

    adj[y].push_back(x);

}

dfs(1,-1);

cnt/=2;

puts(ccc()&&cnt==1?"FHTAGN!":"NO");

return 0;}