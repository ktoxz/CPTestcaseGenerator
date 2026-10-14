#include <iostream>

#include <iomanip>

#include <stdio.h>

#include <vector>

#include <string>

#include <string.h>

#include <stdlib.h>

#include <map>

#define pb push_back

#define ll long long

#define MAX 111111

#define INF 2020202020

using namespace std;



int n, ans = 0;

int P1, P2, P3, T1, T2;

pair < int, int > p[MAX];



int foo ( int &m, int t )

{

	if ( m < t ) t = m;

	m -= t; return t;

}



int main ()

{

	ios_base::sync_with_stdio ( 0 );

	//freopen ( "input.txt", "r", stdin );

	

	cin >> n;

	cin >> P1 >> P2 >> P3 >> T1 >> T2;

	

	for ( int i = 0; i < n; ++ i )

	{

		cin >> p[i].first >> p[i].second;

	}

	

	for ( int i = 0; i < n; ++ i )

	{

		ans += (p[i].second - p[i].first)*P1;

		int temp = p[i+1].first - p[i].second;

		if ( i < n-1 ) ans += P1*foo(temp,T1) + P2*foo(temp,T2) + P3*temp;

	}

	

	cout << ans << endl;

	

	return 0;

}