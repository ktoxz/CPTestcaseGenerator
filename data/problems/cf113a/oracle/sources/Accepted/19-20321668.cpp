/*

	Training Contest 11 : 11 days to University

	http://acm.hust.edu.cn/vjudge/contest/130997#overview

*/



#include <bits/stdc++.h>

using namespace std;

typedef long long int lli;



inline char Case( char c ) { return c < 'a' ? 'A' : 'a'; }

inline char Lower( char c ) { return c < 'a' ? c + 'a' - 'A' : c; }



int main()

{

	vector<char> v;

	string s; int sl;

	bool ok = true;

	while ( cin>>s )

	{

		sl = s.length();

		reverse( s.begin() , s.end() );

		

		if ( s.substr( 0 , 4 ) == "soil" ) v.push_back( 'a' );

		else if ( s.substr( 0 , 5 ) == "alail" ) v.push_back( 'A' );

		else if ( s.substr( 0 , 3 ) == "rte" ) v.push_back( 'n' );

		else if ( s.substr( 0 , 4 ) == "arte" ) v.push_back( 'N' );

		else if ( s.substr( 0 , 6 ) == "sitini" ) v.push_back( 'v' );

		else if ( s.substr( 0 , 6 ) == "setini" ) v.push_back( 'V' );

		else ok = false;

	}

	

	int vs = v.size();

	

	// same gender

	for ( int i=0 ; i<vs ; i++ ) ok &= (Case(v[0]) == Case(v[i]));

	

	// aaa..nvvv.. pattern if isn't a word

	if ( vs > 1 )

	{

		int step = 0;

		for ( int i=0 ; i<vs ; i++ )

		{

			v[i] = Lower( v[i] );

			

			if ( step == 0 )

			{

				if ( v[i] == 'n' ) step++;

				else if ( v[i] != 'a' ) ok = false;

			}

			else if ( step == 1 )

			{

				if ( v[i] == 'v' ) step++;

				else ok = false;

			}

			else if ( step == 2 )

			{

				if ( v[i] != 'v' ) ok = false;

			}

		}

		

		ok &= (step >= 1);

	}

	

	cout<<( ok ? "YES" : "NO" )<<"\n";

	

	return 0;

}