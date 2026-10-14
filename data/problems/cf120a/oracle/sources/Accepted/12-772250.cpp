#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cctype>
#include <string>
#include <cstring>
#include <ctime>
#include <cstring>
#include <fstream>

using namespace std;

#define F first
#define PB(v,x) v.push_back(x)
#define size(X) (int)X.size()
#define S second
#define show(X) cerr << #X << " = " << X << endl;
#define getrandom(min,max) \
	((rand()%(int)(((max)+1)-(min)))+min)
#define foreach(var, container) \
	for(typeof((container).begin()) var = (container).begin(); \
			var != (container).end(); \
			++var)
#define SetBit(value, place) ((value) | (1 << (place)))
#define ClearBit(value, place) ((value) & (~(1 << (place))))
#define ToggleBit(value, place) ((value) ^ (1 << (place)))
#define GetBit(value, place) (((value) >> (place)) & 1)
#define GetPrecentage(Numerator, Denominator)	((Numerator)*100.0/(Denominator))
#define GI ({int t;scanf("%d",&t);t;})
#define GL ({LL t;scanf("%lld",&t);t;})
#define GD ({double t;scanf("%lf",&t);t;})
#define is istringstream
#define os ostringstream
#define lb lower_bound
#define ub upper_bound
#define bs binary_search
#define REP(i,n) for (int i=0,_n=(n); i < _n; i++)
#define REV(i,n) for (int i=(n)-1; i >= 0; i--)
#define FOR(i,a,b) for (int _b=(b), i=(a); i <= _b; i++)
#define ROR(i,a,b) for(int i=(a),_b=(b);i>=_b;i--)
#define ALL(c) (c).begin(), (c).end()
#define SORT(c) sort(ALL(c))
#define CLEAR(x) memset(x,0,sizeof x);
#define REVERSE(c) reverse(ALL(c))
#define UNIQUE(c) SORT(c),(c).resize(unique(ALL(c))-(c).begin())
#define INF 0x7fffffff
#define eps 1.0e-11
template <class X> void printa(X a,int n)
{
	REP(i,n) cerr << a[i] << " " ;
	cerr << endl;
}

template <class X> void printv(X v) 
{
	foreach(it,v) cerr << *it << " " ;
	cerr << endl;
}
typedef pair<int,int> pii;
typedef long long ll;
typedef pair<ll,ll> pll;

ifstream fin("input.txt");
ofstream fout("output.txt.");

int main()
{
	string s;
	int n;
	fin >> s >> n;
	if(s[0]=='f')
	{
		if(n==1)
		{
			fout << "L" << endl;
			return 0;
		}
		else
		{
			fout << "R" << endl;
			return 0;
		}
	}
	else
	{
		if(n==1)
		{
			fout << "R" << endl;
			return 0;
		}
		else
		{
			fout << "L" << endl;
			return 0;
		}
	}
	return 0;
}