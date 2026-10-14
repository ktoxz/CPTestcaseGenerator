#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <vector>
#include <map>
#include <string>
#include <queue>

using namespace std;

// BEGIN TEMPLATE SECTION
typedef long long huge;
typedef vector<int> vi;
typedef vector<vector<int> > vii;
typedef pair<int, int> pi;
typedef vector<pair<int, int> > vpi;
typedef long long big;

#define oo 0x3f3f3f3f
#define fn(_i, _n) for(int (_i) = 0; (_i) < (_n); (_i)++)
#define fi(_n) fn(i, (_n))
#define fj(_n) fn(j, (_n))
#define fk(_n) fn(k, (_n))
#define foreach(_x) for(typeof((_x).begin()) it = (_x).begin(); it != (_x).end(); it++)
#define pb(_x) push_back((_x))
#define sz(_x) ((int)(_x).size())
#define all(_x) (_x).begin(), (_x).end()
#define rall(_x) (_x).rbegin(), (_x).rend()
#define mp(_x, _y) make_pair((_x), (_y))
#define fill(_x, _y) memset((_x), (_y), sizeof(_x))
#define zero(_x) fill(_x, 0)
#define shl(_n) (1<<(_n))
#define lshl(_n) (1LL<<(_n))
// END TEMPLATE SECTION

int mdc(int a, int b)
{
  return(b == 0 ? a : mdc(b, a%b));
}

int faz(int a, int b, int n, int vez)
{
  int g = (vez == 0) ? mdc(n, a) : mdc(n, b);

  if (g > n) return(1-vez);
  return(faz(a,b,n-g,1-vez));
}

int main(void)
{
  int a,b,n;

  scanf("%d %d %d", &a, &b, &n);
  printf("%d\n", faz(a,b,n,0));

  return(0);
}