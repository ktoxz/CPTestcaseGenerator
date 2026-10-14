#include <iostream>

#include <string>

#include <algorithm>

#include <bits/stdc++.h>

#include <stdio.h>

#include <stdlib.h>

using namespace std;

const int Max = 10055;

int gcd( long long a , long long b )

{

    if ( b == 0 )

    return a ;

    else

        return  gcd ( b , a % b ) ;

}

 long long lcm ( long long  a , long long b )

{

    return ( a* ( b / gcd ( a , b ) ) ) ;

}

int a[100005] , x[100005] , c[1000005] ;

int main()

{

     long long  k , l , sum = 0 ;

     cin >> k >> l ;

     // sum = k * k ;

     //cout << 5 * 576 << endl ;

     // cout << sum  << " " << l / sum << " " << l % sum << endl ;

     if ( ( l % k ) !=  0 )

        return cout << "NO" , 0 ;

     else

        {

            while ( l % k == 0 )

            {

                l/=k ;

                sum++ ;

            }

        //cout << "YES" << endl <<  h - 1  ;

        }

        if ( l == 1 )

            cout << "YES" << endl << sum - 1 ;

        else

            cout << "NO" ;

    return 0 ;

}