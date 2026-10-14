#include <iostream>
using namespace std;
int main()
{
    #define int long int
    int n , p1 , p2 , p3 , t1 , t2 , l[105] , r[105] , temp;
    int ans = 0;
    cin >> n >> p1 >> p2 >> p3 >> t1 >> t2;
    for( int i=0 ; i<n ; i++ )
        cin >> l[i] >> r[i];
    if(n)
        for( int i=0 ; ; i++ )
        {
            ans += (r[i]-l[i])*p1;
            if( i==n-1 )
                break;
            temp = l[i+1]-r[i];
            if( temp >= t1+t2 )
            {
                ans += t1*p1 + t2*p2 + (temp - t1 - t2)*p3;
            }
            else if( temp >= t1 )
            {
                ans += (temp -t1)*p2 + t1*p1;
            }
            else
            {
                ans += temp*p1;
            }
        }
    cout << ans << endl;
    return 0;
}