#include <bits/stdc++.h>
using namespace std;
#define lp(i,n) for (int i = 0; i < n; ++i)
#define lp1(i,n) for (int i = 1; i <= n; ++i)
#define rng(i,a,b) for(int i = (a),step = ((a)<=(b))?1:-1,__temp = b+step;i != __temp; i += step)
#ifndef ONLINE_JUDGE
#define eprintf(...) fprintf(stderr,__VA_ARGS__);fflush(stderr);
#else
#define eprintf(...)
#endif // ONLINE_JUDGE
typedef long long ll;
typedef double dbl;
const int inf = 1e9+7;
const ll llinf = 1e18+7;
const dbl eps = 1e-15;
int main(){

    int n;
    scanf("%d",&n);
    ll ans = 0;
    lp1(i,n){
        int x;
        scanf("%d",&x);

        ans += 1ll*(x-1)*i + 1;
    }

    printf("%lld\n",ans);
    return 0;
}