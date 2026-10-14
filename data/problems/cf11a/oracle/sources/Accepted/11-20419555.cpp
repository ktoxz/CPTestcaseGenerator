#define FNAME ""



#include <bits/stdc++.h>



#define hash padjf9srpi

#define y0 sdkfaslhagaklsldk

#define y1 aasdfasdfasdf

#define yn askfhwqriuperikldjk

#define j1 assdgsdgasghsf

#define tm sdfjahlfasfh

#define lr asgasgash

#define pb push_back

#define mp make_pair

#define forn(i, n) for (int i = 0; i < (n); i++)

#define fornr(i, n) for (int i = (n) - 1; i >= 0; i--)

#define forab(i, a, b) for (int i = (a); i < (b); i++)

#define gcd __gcd

#define all(a) (a).begin(), (a).end()

 

#ifdef _WIN32

    #define I64 "%I64d"

#else

    #define I64 "%lld"

#endif



using namespace std;



typedef long long LL;

typedef unsigned long long ULL;

typedef long double LD;

typedef pair <int, int> pii;                                                                                                                                                                                      

typedef vector <int> vi;



template <class T> T sqr(const T &a) {return a * a;}



int n, d;

LL a[30000];



int main()

{

#ifdef LOCAL

    freopen(FNAME".in", "r", stdin);

    freopen(FNAME".out", "w", stdout);

#endif

    LL ans = 0;

    scanf("%d%d", &n, &d);

    forn(i, n) {

        scanf("%lld", &a[i]);

    }

    forab(i, 1, n) {

        if (a[i] > a[i - 1])

            continue;

        LL x = (a[i - 1] - a[i]) / d + 1;

        ans += x;

        a[i] += x * d;

    }

    printf("%lld\n", ans);

}