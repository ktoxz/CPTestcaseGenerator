#include <iostream>

#include <cstdio>

#include <cmath>

using namespace std;



main()

{



    long long a[50000] , n , ans = 0;

    cin>>n;

    n = abs(n);



    for(long long i=0 ; i<=45000 ; i++)

    {

        a[i] = i*(i+1) / 2;

    }

    int i = 0;

    for(i=0 ; i<=45000 ; i++)

    {

        if( (a[i]>=n && (a[i]-n)%2==0 ))

        {

            cout<<i<<endl;

            return 0;

        }

    }



    return 0;

}