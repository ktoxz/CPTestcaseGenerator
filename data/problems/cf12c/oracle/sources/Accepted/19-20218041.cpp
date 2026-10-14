#include <bits/stdc++.h>



using namespace std;



#define ll long long

#define ull unsigned long long

#define erep(i, x, n) for (int i = x; i<=(int)(n); i++)

#define rep(i, x, n) for(int i = x; i<(int)(n); i++)

#define vi vector<int>

#define vii vector< pair<int, int> >

#define vvi vector< vi >

#define vll vector<long long>

#define vc vector<char>

#define vb vector<bool>

#define vvii vector< vector< pii > >

#define pii pair<int, int>

#define mapii map<int, int>

#define mapsi map<string, int>

#define INF  LLONG_MAX

#define all(v) ((v).begin()), ((v).end())

#define sz(v) ((int)((v).size()))

#define pie  acos(-1)

#define mod(n,m) ((n % m + m) % m)

#define eps (1e-9)

#define reset(n, m) memset(n, m, sizeof n)

#define endl '\n'



int main()

{

    ios_base::sync_with_stdio(false);

    cin.tie(0);

    int n, m;

    cin >> n >> m;

    vi vec(n);

    rep(i, 0, n) cin >> vec[i];

    sort(all(vec));

    mapsi mp;

    set<string> st;

    vector< pair<int, string> > hoba;

    rep(i, 0, m)

    {

        string x;

        cin >> x;

        st.insert(x);

        mp[x]++;

    }

    while(!st.empty())

    {

        hoba.push_back({mp[*st.begin()], *st.begin()});

        st.erase(st.begin());

    }

    sort(all(hoba));

    int mn = 0, mx = 0, temp = n-1;

    for(int i = sz(hoba)-1; i>=0; i--) mx += hoba[i].first*vec[temp--];

    temp = 0;

    for(int i = sz(hoba)-1; i>=0; i--) mn += hoba[i].first*vec[temp++];

    cout << mn << " " << mx;

    return 0;

}