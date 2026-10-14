#include<bits/stdc++.h>



using namespace std;



vector< vector<int> >graph;



int ans;



void dfs(int s,int c){

    if(c>ans)ans=c;

    for(int i=0;i<graph[s].size();i++){

        dfs(graph[s][i],c+1);

    }

}



int main()

{

    int n,t,i;

    cin>>n;

    graph.resize(n+1);

    for(i=1;i<=n;i++){

        cin>>t;

        if(t!=-1){

            graph[t].push_back(i);

        }

    }

    ans=0;

    for(i=1;i<=n;i++){

        dfs(i,1);

    }

    cout<<ans;

    return 0;

}