#define _CRT_SECURE_NO_WARNINGS

#include<iostream>

#include<string>

#include<string.h>

#include<sstream>

#include<queue>

#include<set>

#include<stack>

#include<vector>

#include<bitset>

#include<iomanip>

#include<algorithm>

#include<cmath>

#include<map>

#include<functional>



template< class T>

T gcd(T a, T b) { return b == 0 ? a : gcd(b, a % b); }

template< class T>

T lcd(T a, T b) { return b*(a / gcd(a, b)); }

template<class T>

T  t_sum(T a) { return (a*(a + 1)) / 2; }

#define fo(i,m,n) for(int i = m ; i < n ; i++)

#define pii pair<int ,int>

#define gt(n) scanf("%d",&n)

#define gtl(n) scanf("%lld" ,&n)

#define ii pair<int,int>



using namespace std;



string s;

int rem = 0;

int ans = 0;

int main()

{

	cin >> s;

	if (s.size() == 1)

	{

		cout << 0;

		return 0;

	}

	fo(i, 0, s.size())

	{

		rem += int(s[i]) - 48;

	}

	ans++;

	s = to_string(rem);

	while (rem > 9)

	{

		s = to_string(rem);

		rem = 0;

		fo(i, 0, s.size())

		{

			rem += int(s[i]) - 48;

		}

		ans++;

	}

	cout << ans;

	return 0;

}