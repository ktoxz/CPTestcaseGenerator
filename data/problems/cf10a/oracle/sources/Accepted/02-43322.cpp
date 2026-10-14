#include <stdio.h>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>
#include <iostream>
#include <map>
#include <math.h>
#include <set>
#include <queue>
using namespace std;
typedef long long LL;
#define INF 2000000000
#define SZ(v) ((int)(v).size())
#define FOR(i,a,b) for(int i=(a);i<(b);i++)
#define FORE(i,a,b) for(int i=(a);i<=(b);i++) 
#define FS first
#define SD second
#define MP make_pair
#define FF fflush(stdout);

bool jest[2000];

int main(){
	int n,p1,p2,p3,t1,t2;
	scanf("%d%d%d%d%d%d",&n,&p1,&p2,&p3,&t1,&t2);
	FOR(i,0,2000) jest[i] = false;
	int kon = 0;
	FOR(i,0,n){
		int a,b;
		scanf("%d%d",&a,&b);
		FOR(j,a,b) jest[j] = true;
		kon = b;
	}
	int ret = 0;
	int pocz = 0;
	FOR(i,0,2000){
		if(jest[i]){
			pocz = i;
			break;
		}
	}
	int tryb = 0,czas =0;
	FOR(i,pocz,kon){
		
		if(jest[i]){
			tryb = 0;
			ret+=p1;
			czas = 0;
		}
		else{
			
			if(tryb==0) ret+=p1;
			else if(tryb==1) ret+=p2;
			else ret+=p3;
			czas++;
			if(czas==t1) tryb = 1;
			else if(czas==t2+t1) tryb = 2;
		}
	}
	printf("%d\n",ret);
	
}