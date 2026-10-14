/***************************************************\

*               Mir Abdullah yousuf                 *

*    Khulna University of Engineering & Technology  *

*     Electrical and Electronic Engineering, 2k14   *

\***************************************************/

#include <bits/stdc++.h>

#define LL              long long

#define PI              acos(-1.0)

#define MS(a,b)         memset(a, b, sizeof (a))

#define sf(a)           scanf("%d", &a)

#define sff(a, b)       scanf("%d %d", &a, &b)

#define sfff(a, b, c)   scanf("%d %d %d", &a, &b, &c)

#define sfl(a)          scanf("%lld", &a)

#define sfll(a, b)      scanf("%lld %lld", &a, &b)

#define sflll(a, b, c)  scanf("%lld %lld %lld", &a, &b, &c)

#define READ()          freopen("input.txt", "r", stdin)

#define WRITE()         freopen("output.txt", "w", stdout)

#define GCD(a, b)       __gcd(a, b)

#define sqr(a)          (a) * (a)

#define MOD

using namespace std;





int main()

{

    LL k, l;

    sfll(k, l);



    LL x = k, cnt = 0;



    while (k <= l) {

        if (k == l) {

            printf("YES\n");

            printf("%lld\n", cnt);

            return 0;

        }

        k = k * x;

        cnt++;

    }

    printf("NO\n");

    return 0;

}