/*

    Rem is cute :D

*/



# include <bits/stdc++.h>



using namespace std;



#define pii pair<int, int>

#define pll pair<ll, ll>



#define pb push_back

#define eb emplace_back

#define mp make_pair



#define fi first

#define se second



#define y0 asjdlksajldjals

#define y1 ajsldjalksdkjlk



typedef long long ll;

typedef long double ld;

typedef unsigned long long ull;



const int inf = (int)1e9 + 7;

const int maxn = (int)6e5 + 7;

const int lmaxn = (int)6e6 + 7;

const ll linf = (ll)1e16 + 7;



const ld eps = ld(1e-11);



const ll dx[] = {-1, 0, 0, 1};

const ll dy[] = {0, -1, 1, 0};



ll gcd(ll a, ll b){

    while(b) a %= b, swap(a, b);

    return a | b;

}



ll lcm(ll a, ll b){

    return a * b / gcd(a, b);

}

bool isprime(ll x)

{

    ll q = 0;

    for(ll i = 2; i * i <= x; i++)

    {

        if(x % i == 0)

        {

            return false;

        }

    }

    return true;

}



ll n, ans, k, res, m, q, z;

ll cnt[256], sz;

set < ll > s, ss;

vector < ld > v, t[311111];

ll a[1111][1111], b[maxn];

ll ati[1001][1001];



ll bp(ll x){

    for(ll i = 1; i <= n; i++)

    {

        for(ll j = 1; j <= m; j++)

        {

            ati[i][j] = 0;

        }

    }

    for(ll i = 1; i <= n; i++)

    {

        vector < int > one;

        for(ll j = 1; j <= m; j++)

        {

            if(a[i][j] >= x)

                one.pb(j);

        }

        for(int f = 0; f < (int)one.size(); ++f){

            for(int s = f + 1; s < (int)one.size(); ++s){

                if(ati[one[f]][one[s]])

                    return 1;

                ati[one[f]][one[s]] = 1;

            }

        }

    }

    return 0;

}

int main(){

    cin >> n;

    cin >> k;

    if(k % n != 0)

    {

        cout << "NO";

        return 0;

    }



    while(1)

    {

        if(k == n)

        {

            break;

        }

        k /= n;

        ans++;

        if(k % n != 0)

        {

            cout << "NO";

            return 0;

        }

    }

    cout << "YES" << "\n";

    cout << ans;

}