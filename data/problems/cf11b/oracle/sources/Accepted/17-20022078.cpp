#include <bits/stdc++.h>

using namespace std;

typedef long long int lli;



int main()

{

	int n; cin>>n;

	n = abs( n );

	int ans[4] = { 0 , 1 , 3 , 2 };

	if ( n < 4 ) { cout<<ans[n]<<"\n"; return 0; }

	

	int now = 0 , sol;

	for ( int i=1 ; i<=n ; i++ )

	{

		now += i;

		if ( now == n ) { sol = i; break; }

		if ( now > n )

		{

			int dif = now - n;

			

			if ( dif % 2 == 0 )		// we can make negative number dif/2

				sol = i;

			else					// we can go forward until dif became even and then ...

				sol = i + 1 + ((i+1)%2==0);

			

			break;

		}

	}

	

	cout<<sol<<"\n";

	return 0;

}