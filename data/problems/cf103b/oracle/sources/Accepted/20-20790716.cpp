#include <bits/stdc++.h>

using namespace std;

vector< vector<int> > v;

int cycle=0;int c=0;

int vis[1000];

int dfs(int node,int oldnode){

if(vis[node])

    return 0;

vis[node]=1; c++;

 for(int i=0;i<v[node].size();i++){

    if(vis[v[node][i]]==1&&v[node][i]!=oldnode)

        { cycle++;}

    //cout<<v[node][i]<<" "<<node<<endl;

    dfs(v[node][i],node);

 }

}

int main(){

  int n,m,a=0,b;

  cin>>n>>m;

  v.resize(n+1);

   for(int i=0;i<m;i++)

    {

    cin>>a>>b;

    v[a].push_back(b);

    v[b].push_back(a);

    }



    dfs(a,0);

    if(c==n&&cycle==2)

        cout<<"FHTAGN!"<<endl;

    else

    cout<<"NO"<<endl;



  // cout<<c<<cycle<<endl;

}