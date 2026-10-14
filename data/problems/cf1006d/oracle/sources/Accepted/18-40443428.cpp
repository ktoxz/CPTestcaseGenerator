#include <bits/stdc++.h>

#define ll long long int
#define f first
#define s second
#define a7laInputDaWlaEh ios_base::sync_with_stdio(0);cin.tie(0);
#define pb push_back

using namespace std;

///const long double eps = 1e-9;
///int dX[8]={1,0, 0,-1,-1,-1, 1,1};
///int dY[8]={0,1,-1, 0,-1, 1,-1,1};
///int dx[4]={1,0, 0,-1};
///int dy[4]={0,1,-1, 0};

/*ll modPower(ll base ,ll power, ll mod){
	if(power == 0) return (ll)1;
	if(power % 2 == 0) return modPower((base*base)%mod, power/2, mod)%mod;
	return (base * modPower((base*base)%mod, power/2, mod)%mod)%mod;
}*/

///Extended Euclidean Algorithm (CoPrimes)
///Calculate inverse Modulus
///if a is the number I want then x is the answer
/*ll gcdExtended(ll a, ll b, ll *x, ll *y)
{
    // Base Case
    if (a == 0) {
        *x = 0;
        *y = 1;
        return b;
    }
    ll x1, y1; // To store results of recursive call
    ll gcd = gcdExtended(b%a, a, &x1, &y1);
    // Update x and y using results of recursive call
    *x = y1 - (b/a) * x1;
    *y = x1;
    return gcd;
}*/


int main()
{
    ///freopen("input.txt","r",stdin);
    ///freopen("output.txt","w",stdout);
    ///readString scanf("%s", charArrName);
    a7laInputDaWlaEh;
    int n, sw;
    cin >> n;
    string a, b;
    cin >> a >> b;
    for(int i = 0; i < n; i++)
    {
        if(a[i] == b[i]) continue;
        sw = n - 1 - i;
        if(a[sw] == b[sw]) continue;
        if(i == sw) continue;
        if(a[i] == a[sw])
        {
            if(b[i] == b[sw])
            {
                swap(a[i], b[i]);
                swap(a[i], a[sw]);
            }
        }
        else
        {
            if(b[i] == b[sw]){
                swap(a[i], b[i]);
                swap(a[i], a[sw]);
            }
            else if(a[i] == b[sw] || a[sw] == b[i])
                swap(a[i],a[sw]);
        }
        /*cout << "iiiii" << i << endl;
        cout << "************" << endl;
        cout << a << endl << b << endl;
        cout << "************" << endl;*/
    }
    int ans = 0;
    //cout << a << endl << b << endl;
    for(int i = 0; i < n; i++)
        if(a[i] != b[i]) ++ans;
    cout << ans << endl;
    return 0;
}