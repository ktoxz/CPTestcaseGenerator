#include<cstdio>
#include<iostream>
#include<sstream>
#include<cmath>
#include<algorithm>
#include<map>
#include<set>
#include<list>
#include<vector>
#include<stack>
#include<queue>
#include<string>
#include<ctime>
#include<iomanip>
#include<fstream>
using namespace std;
typedef vector<int> VI;
typedef vector<VI> VVI;
typedef pair <int,int> ii;
typedef long long LL;
#define sz(a) int((a).size())
#define pb push_back
const int INF = 2147483647;
const double PI = 3.141592653589793;

int n,tab[2005],r,maxx,i,j;

int main () {
scanf ("%d",&n);
for (i=0;i<n;i++) {
    scanf ("%d",&tab[i]);
    tab[i]--;
}
maxx=0;
for (i=0;i<n;i++) {
    j=i; r=0;
    while (j!=-2) {
          j = tab[j]; r++;
    } 
    maxx=max(maxx,r);
}
printf("%d\n",maxx);
return 0;
}