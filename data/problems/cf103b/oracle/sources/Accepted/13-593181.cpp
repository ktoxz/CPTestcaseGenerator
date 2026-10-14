/*
** Khamitbekov Madi
** Kazakhstan, Almaty
** Kazakh-Turkish High School, 2011
*/
#include <algorithm>
#include <iostream>
#include <string.h>
#include <utility>
#include <fstream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <cassert>
#include <vector>
#include <cstdio>   
#include <cmath>
#include <queue>
#include <ctime>
#include <list>
#include <set>
#include <map>

using namespace std;

typedef long long ll;
typedef long double ld;
typedef unsigned long long ull;
typedef vector < vector < int > >  vvi;
typedef vector < pair < int, int > >  vpi;
typedef queue  < pair < int, int > > qpi;

#define abs(x) ((x) > 0 ? (x) : -(x))
#define all(v) (v).begin(), (v).end()
#define sq(x) ((x)*(x))
#define len length()
#define pb push_back
#define mp make_pair
#define inf 7777777
#define eps (1e-7)
#define sz size()
#define s second
#define f first
 
vector <int> a[200];
int c[200][200]; 
int n;
int u[200];
int p[200];
int cc[200];
bool cycle;
void dfs (int x, int pr = -1) {
   u[x] = 1;
   p[x] = pr;
   if (cycle) return;
   for (int i = 0; i < a[x].sz; i++) {
      int j = a[x][i];
      if (j == pr || !c[x][j]) continue;
      if (u[j] == 1) {
            cycle = 1;
            int id = x;
            c[x][j] = c[j][x] = 0;
            cc[j] = 1;
            while (id != j)cc[id] = 1,  c[p[id]][id] = c[id][p[id]] = 0,id = p[id];
            return;
      }
      if (!u[j]) {
       dfs (j,x);
        if (cycle) return;
      }
   }
   u[x] = 2;
}
void dfs1 (int x) {
   u[x] = 1;
   for (int i = 0; i < a[x].sz; i++)
      if (!u[a[x][i]])dfs1 (a[x][i]);
}
int main ()
{
   int m, x, y;
   cin >> n >> m;
   if (n < 3) {
      cout << "NO";
      return 0;
   }
   for (int i = 0; i < m; i++)   cin >> x >> y, x--, y--, c[x][y] = c[y][x] = 1, a[x].pb(y), a[y].pb(x);
   cycle = 0;
   dfs1 (0);
   for (int i = 0; i < n; i++)
      if (!u[i]) {
         cout << "NO";
         return 0;
      }else u[i] = 0;
   dfs (0);
   if (!cycle) {
      cout << "NO";
      return 0;
   }
   cycle = 0;
   int k = 0;
   for (int i = 0; i < n; i++) u[i] = 0;
   for (int i = 0; i < n; i++) {   
      if (cc[i]) {
         if (u[i]) {
            cout << "NO";
            return 0;
         }
         dfs (i);
      }     
   }
   for (int i = 0; i < n; i++)
      if (!u[i]) {
         cout << "NO";
         return 0;
      }
   
   if (cycle) {
      cout << "NO";
      return 0;
   }
   cout << "FHTAGN!";
   return 0;
}