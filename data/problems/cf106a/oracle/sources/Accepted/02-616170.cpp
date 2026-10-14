/* BDFHJK
 * Mon, 09 May 2011 17:53:14 +0200 */

#include<iostream>
#include<cstdio>
#include<string>
#include<list>
#include<deque>
#include<map>
#include<set>
#include<queue>
#include<stack>
#include<utility>
#include<sstream>
#include<cstring>
#include<cmath>
#include<cstdlib>
#include<algorithm>
#include<vector>

using namespace std;

#define DEBUG 1
#define DB(X) printf("Debug: %d\n", X);

#define REP(I,N) for(int I=0;I<(N);I++)
#define FOR(I,A,B) for(int I=(A);I<=(B);I++)
#define FORD(I,A,B) for(int I=(A);I>=(B);I--)
#define ALL(X) (X).begin(),(X).end()
#define FOREACH(I,C) for(VAR(I,(C).begin());I!=(C).end();I++)

#define MOD ((int)1e9+7)
#define INF ((int)1e9+7)
#define mINF ((int)1e6+7)
#define EPS 1e-8

#define VAR(V,init) __typeof(init) V=(init)
#define SIZE(X) X.size()

#define PB push_back
#define MP make_pair
#define FI first
#define SE second

typedef vector<int> VI;
typedef pair<int,int> PII;
typedef long long LL;
typedef vector<string> VS;

LL nwd(LL a, LL b) { return !b?a:nwd(b,a%b); }

int rankA;
int suitA;
int rankB;
int suitB;
int tramp;

int value(char a)
{
	if (a=='6') return 1;
	if (a=='7') return 2;
	if (a=='8') return 3;
	if (a=='9') return 4;
	if (a=='T') return 5;
	if (a=='J') return 6;
	if (a=='Q') return 7;
	if (a=='K') return 8;
	if (a=='A') return 9;
	
	if (a=='S') return 1;
	if (a=='H') return 2;
	if (a=='D') return 3;
	if (a=='C') return 4;
	
	return -1;
}

int main()
{
	char b;
	b = getchar();
	tramp = value(b);
	b = getchar(); //space
	b = getchar(); 
	rankA = value(b);
	b = getchar(); 
	suitA = value(b);
	b=getchar(); //space
	b=getchar();
	rankB = value(b);
	b=getchar();
	suitB = value(b);
	
	//printf("%d %d %d %d %d\n", rankA, suitA, rankB, suitB, tramp);
	
	bool yes = 0;
	if (suitA == suitB && rankA > rankB) yes = 1;
	if (suitA == tramp && suitB != tramp) yes = 1;
	
	if (yes) printf("YES\n"); else printf("NO\n");

}