#include <bits/stdc++.h>



#define sr(s) sort(s.begin(), s.end())

#define rs(s) reverse(s.begin(), s.end())

#define sz(s) s.size()

#define pb push_back

#define mp make_pair



using namespace std;



typedef long long ll;



const int N = 1e5 + 15;

const int MXN = 1e3 + 15;



char ch;



string s, s1;



int x, y;



main()

{

   ios_base::sync_with_stdio(0);

   cin.tie(0);

   

   cin >> ch;

   cin >> s >> s1;

   if (s[0] >= '6' && s[0] <= '9')

   	x = s[0] - 48;

   if (s[0] == 'T')

   	x = 10;

   if (s[0] == 'J')

   	x = 11;

   if (s[0] == 'Q')

   	x = 12;

   if (s[0] == 'K')

   	x = 13;

   if (s[0] == 'A')

   	x = 14;

   if (s1[0] >= '6' && s1[0] <= '9')

   	y = (s1[0] - 48);

   if (s1[0] == 'T')

   	y = 10;

   if (s1[0] == 'J')

   	y = 11;

   if (s1[0] == 'Q')

   	y = 12;

   if (s1[0] == 'K')

   	y = 13;

   if (s1[0] == 'A')

   	y = 14;

   if (ch == s[1])

   {

   	if (ch != s1[1])

   	{

   		cout << "YES";

   		return 0;

		}

		if (ch == s1[1])

		{

			if (x > y)

			{

				cout << "YES";

				return 0;

			}

			cout << "NO";

			return 0;

		}

	}

	if (ch != s[1] && s[1] != s1[1])

	{

		cout << "NO";

		return 0;

	}

	if (s[1] == s1[1])

	{

		if (x > y)

		{

			cout << "YES";

			return 0;

		}

		cout << "NO";

		return 0;

	}

	return 0;

}