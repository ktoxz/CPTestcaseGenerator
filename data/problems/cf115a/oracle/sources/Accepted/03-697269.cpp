#include<cstdio>
#include<cctype>
#include<cstring>
#include<cmath>
#include<cstdlib>
#include<ctime>
#include<cassert>
#include<iostream>
#include<sstream>
#include<string>
#include<vector>
#include<list>
#include<deque>
#include<stack>
#include<queue>
#include<bitset>
#include<map>
#include<set>
#include<complex>
#include<algorithm>
#include<functional>
#include<utility>
using namespace std;
#define PB push_back
#define MP make_pair
#define SZ(V) ((int)((V).size()))
typedef long long LL;
typedef unsigned long long ULL;
#define FEACH(I,S)		for(__typeof((S).begin()) I=(S).begin();I!=(S).end();++I)
#define REP(I,N)		for(I=0;I<(N);++I)
#define FN(I,N)			for(I=1;I<=(N);++I)
#define RREP(I,N)		for(I=(N)-1;I>=0;--I)
#define RFN(I,N)		for(I=(N);I;--I)
#define FAB(I,A,B)		for(I=(A);I<=(B);++I)
vector<int> son[2048];
int f[2048];
void dfs(int x){
	int& ret = f[x];
	FEACH(s,son[x]){
		dfs(*s);
		ret = max(ret,f[*s]);
	}
	++ret;
}
int main(){
	int n,i,t;
	scanf("%d",&n);
	FN(i,n){
		scanf("%d",&t);
		if(t>0)son[t].PB(i);
		else son[0].PB(i);
	}
	dfs(0);
	printf("%d\n",f[0]-1);//while(1);
	return 0;
}