#include <bits/stdc++.h>
using namespace std;
// #defines
#define MOD 1000000007
#define MAX 1000000
#define M5 100001
#define endl "\n"
#define FOR(i, a, b) for (int i = (a); i < (b); i++)
#define rep(i, begin, end) for (__typeof(end) i = (begin) - ((begin) > (end)); i != (end) - ((begin) > (end)); i += 1 - 2 * ((begin) > (end)))
#define trep  \
    int t;    \
    cin >> t; \
    while (t--)
#define all(c) (c).begin(), (c).end()
#define MP(x, y) make_pair((x), (y))
#define PB(X) push_back(X)
#define MT make_tuple
#define EB emplace_back
#define ff first
#define ss second
#define isPow2(x) (x && (!(x & (x - 1))))
#define last_bit(n) (n & (-n))
#define abs(x) ((x < 0) ? -(x) : x)
#define mset(m, v) memset(m, v, sizeof(m))
#define tr(c, it) for (typeof((c).begin()) it = (c).begin(); it != (c).end(); it++)
#define present(c, x) ((c).find(x) != (c).end())      //SET/MAP
#define vpresent(c, x) (find(all(c), x) != (c).end()) //VECTOR
#define cer(x) cerr << #x << ": " << x << endl;       //error
#define imax numeric_limits<int>::max()
#define imin numeric_limits<int>::min()
#define ldmax numeric_limits<ld>::max()
#define ldmin numeric_limits<ld>::min()
#define lldmax numeric_limits<lld>::max()
#define lldmin numeric_limits<lld>::min()
//typedefs
typedef long long ll;
typedef vector<int> vi;
typedef pair<int, int> pii;
typedef vector<pii> vpii;
typedef vector<ll> vll;
typedef pair<ll, ll> pll;
typedef vector<pll> vpll;
//vector I/O templates
template <typename T>
ostream &operator<<(ostream &o, vector<T> v)
{
    if (v.size() > 0)
        o << v[0];
    for (unsigned i = 1; i < v.size(); i++)
        o << " " << v[i];
    return o << endl;
}
template <typename T>
istream &operator>>(istream &in, vector<T> &v)
{

    for (unsigned i = 0; i < v.size(); i++)
        in >> v[i];
    return in;
}

int main()
{
    ios_base::sync_with_stdio(false);
#ifdef IO1495
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
#endif
    // var "t" declared if using trep
    string s; cin>>s;
    ll sum=0,cnt=0,c1=0,c2=0;
    FOR(i,0,s.size()) {
        ll k=s[i]-'0';
        if(k%3==0){
            cnt++;
            // sum=0;
            c1=c2=0;
            // cer(c1); cer(c2);
        } else {
            // sum=sum+k;
            k=k%3;
            if(k==1)
             c1++;
            else
             c2++;
            // k==1?c1++:c2++;
            // cer(c1); cer(c2);
            if(c1>=3 || c2>=3){
                cnt++;
                c1=0;c2=0;
            } else if(c1>=1 && c2>=1){
                cnt++;
                c1=0; c2=0;
            }
            // if(sum%3==0){
            //     cnt++;
            //     sum=0;
            // }
        }
    }
    cout<<cnt<<endl;
}