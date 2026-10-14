#include <bits/stdc++.h>



using namespace std;



const int inf = (int)(1e9) + 100;

const int mod = (int)(1e9) + 7;

const int N = (int)(1e5) + 100;



#define pb push_back

#define mp make_pair

#define sz(a) (int)(a.size())

#define all(a) a.begin(), a.end()

#define ff first

#define ss second

#define ll long long

#define pii pair <int, int>

#define pll pair <ll, ll>

#define vi vector <int>

#define vll vector <ll>

#define vpi vector <pii>

#define vpl vector <pll>

#define sc1(a) scanf("%d", &a)

#define sc2(a, b) scanf("%d%d", &a, &b)

#define frw(i, p, n) for(int i = p; i <= n; i++)

#define bck(i, n, p) for(int i = n; i >= p; i--)

#define mem(a) memset(a, 0, sizeof(a))

#define forit(it, s) for(__typeof(s.begin()) it = s.begin(); it != s.end(); it++)



inline int read(){

	int x; cin >> x; return x;

}



inline void out(int x){

	cout << x << ' ';

}



string n;

ll res = 0, ans = 0;



string conv(string s){

	res = 0;

	for(int i = 0; i < sz(s); i++){

		res += int(s[i]-'0');

	}

	string t = "";

	while(res > 0){

		ll k =  res%10;

		t += char(k + '0');

		res/=10;

	}

	reverse(all(t));

	return t;

}

int main(){

	ios_base::sync_with_stdio(false);

	cin.tie(NULL);

	cin >> n;

	if(sz(n) == 1) return cout << 0, 0;

	while(sz(n)!=1){

		ans++;

		n = conv(n);	

	}

	cout << ans;

	return 0;



}