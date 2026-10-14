#include <iostream>
#include <cstdio>
#include <vector>
#include <algorithm>

using namespace std;

#define abs(n) ((n)<(0)?(-(n)):(n))
#define mp make_pair
#define pb push_back
#define f first
#define s second
vector <pair <int,int> > g[1010];
vector <pair <pair <int,int>,int> > ans;
int used[1010],cur=-1;
bool d[1010];
int dfs(int v)
{
    used[v]=1;
    cur=v;
    int mini=1<<29;
    for(size_t i=0;i<g[v].size();i++)
        if (used[g[v][i].f]==1)
                mini=-1;
        else if (!used[g[v][i].f]) mini=min(mini,min(dfs(g[v][i].f),g[v][i].s));
    used[v]=2;
    return mini;
}

int main()
{
    int n,p,a,b,w;
    cin>>n>>p;
    for(int i=0;i<p;i++)
    {
        cin>>a>>b>>w;
        g[--a].push_back(make_pair(--b,w));
        d[b]=true;
    }
    for(int i=0;i<n;i++)
        if (!used[i] && !d[i])
        {
            int t=dfs(i);
            if (t!=-1 && i!=cur)
                ans.pb(mp(mp(i+1,cur+1),t));
        }
    sort(ans.begin(),ans.end());
    cout<<ans.size()<<endl;
    for(size_t i=0;i<ans.size();i++)
        cout<<ans[i].f.f<<" "<<ans[i].f.s<<" "<<ans[i].s<<endl;
    return 0;
}