#include <algorithm>
#include <cstdlib>
#include <cstdarg>
#include <cassert>
#include <cstring>
#include <complex>
#include <cstdio>
#include <vector>
#include <string>
#include <queue>
#include <set>
#include <map>

using namespace std;

typedef long long int64;
typedef long long ll;
typedef long double d64;

#define all(c) (c).begin(),(c).end()
#define sz(c) (int)(c).size()

#define pb push_back
#define mp make_pair
#define fs first
#define sc second
#define y1 y1_gedjcdgfce
#define y0 y0_sadasdasdsa
#define ws ws_sadsadsada

#define eprintf(...) {fprintf(stderr,__VA_ARGS__),fflush(stderr);}

#define forn(i,n) for( int i = 0 ; i < (n) ; i++ )
#define forit(it,c) for( __typeof((c).begin()) it = (c).begin() ; it != (c).end() ; it++ )

#ifdef WIN32
#define INT64 "%I64d"
#else
#define INT64 "%lld"
#endif

#define TASK "task"

int main(){
	//assert(freopen(TASK".in","rt",stdin));
	//assert(freopen(TASK".out","wt",stdout));
	int n;
	int ak = (int)1e9;
	int am = (int)1e9;
	scanf("%d",&n);
	for(int k = 0 ; 4*k <= n ; k++ ){
		int m = n - 4*k;
		if(m%7!=0) continue;
		m /=7;
		if(k+m<ak+am||(k+m==ak+am)&&(k>ak)){
			ak = k;
			am = m;
		}
	}
	if(ak+am>((int)1e9)) return 0*printf("-1\n");
	forn(i,ak) printf("%d",4);
	forn(i,am) printf("%d",7);
	printf("\n");
	return 0;
}