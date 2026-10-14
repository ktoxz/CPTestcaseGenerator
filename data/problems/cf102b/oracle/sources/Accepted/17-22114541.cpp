/**********************************************************************

 *                  BISMILLAHIR RAHMANIR RAHIM                        *

 *                                                                    *

 * "There's a benefit to losing, you get to learn from your mistakes" *

 *                   "Let bygones be bygones"                         *

 *                      "Hope for the best"                           *

 *            "Give your best and Let Karma do the rest"              *

 **********************************************************************/



#include<bits/stdc++.h>



using namespace std;



#define si(x) scanf("%d",&x)

#define sii(x,y) scanf("%d %d",&x,&y)

#define siii(x,y,z) scanf("%d %d %d",&x,&y,&z)

#define sl(x) scanf("%lld",&x)

#define sll(x,y) scanf("%lld %lld",&x,&y)

#define slll(x,y,z) scanf("%lld %lld %lld",&x,&y,&z)

#define ss(ch) scanf("%s",ch)

#define chr getchar()

#define pi(x) printf("%d",x)

#define pii(x,y) printf("%d %d",x,y)

#define pl(x) printf("%lld",x)

#define pll(x,y) printf("%lld %lld",x,y)

#define ps(ch) printf("%s",ch)

#define pc(ch) printf("%c",ch)

#define sf scanf

#define pf printf

#define pcs(x,y) printf("Case %d: %s", x, y)

#define pci(x,y) printf("Case %d: %d", x, y)

#define NL printf("\n")

#define nl '\n'

#define debug(x) printf("Debug  %d !!\n",x)

#define mod 1000000007

#define FI freopen("in.txt","r",stdin)

#define FO freopen("out.txt","w",stdout)



#define FOR(i,j,k) for(i = j; i < k; i++)

#define rep(l,n) FOR(l,0,n)

#define REV(i,j,k) for(i = j; i > k; i--)



#define PI acos(-1.0)

#define INF_MAX 2147483647

#define INF_MIN -2147483647



#define pb(x) push_back(x)

#define ppb() pop_back()

#define sz(x) x.size()

#define xx first

#define yy second

#define mp(a,b) make_pair(a,b)



#define mem(ara,val) memset(ara,val,sizeof(ara))

#define clr(ara) mem(ara,0)

#define st(ara) mem(ara,-1)

#define all(a) a.begin(),a.end()



#define ssz(a) strlen(a)

#define eps 1e-9



typedef long long LL;

typedef unsigned long long ULL;

typedef vector<int> VI;

typedef pair<int,int> PII;

typedef vector< PII > VII;



///=>=>=>=>=>=>=>=>=>00100<=<=<=<=<=<=<=<=<=///



//#define CFw



char a[1000000];



int main(){

    //std::ios_base::sync_with_stdio(0);

    #ifdef CFw

        while(1){

    #endif

    //FI;//FO;



    int t, z = 0, l, i = 0, len;



    int n, k = 0, m = 0, bam = 0, dan = 0, ans = 0;



    string s;



    ss(a);



    s = a;



    while(sz(s) > 1){

        ans++;



        int sum = 0;



        rep(l,sz(s))

            sum += s[l] - '0';



        s.clear();



        while(sum){

            s += (sum % 10) + '0';

            sum /= 10;

        }



        reverse(all(s));

    }



    pi(ans);



    #ifdef CFw

    NL;

    }

    #endif



    return 0;

}