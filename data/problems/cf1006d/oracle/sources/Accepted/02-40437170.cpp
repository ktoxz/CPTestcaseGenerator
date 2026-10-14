#include <iostream>
#include <stdio.h>
#include <algorithm>
#include <vector>
using namespace std ;

#define fi( a , b , c ) for ( int a = b ; a <= c ; a++ )
#define fo( a , b , c ) for ( int a = b ; a >= c ; a-- )
#define long long long

const int N = 1e5+1 ;

string s ;
int n , ans ;
int a[N] , b[N] ;
vector<int> ds ;

void Solve( int l , int r ){
     sort(ds.begin(),ds.end()) ;
     if ( ds[0] == ds[1] && ds[2] == ds[3] ) return ;

     if ( a[l] == b[l] || a[l] == b[r] ){
          ans++ ; return ;
     }
     if ( a[r] == b[l] || a[r] == b[r] ){
          ans++ ; return ;
     }
     if ( b[l] == b[r] ){
          ans++ ; return ;
     }
     ans += 2 ;
}

int main(){

     cin >> n ;
     cin >> s ;
     fi( i , 1 , n ) a[i] = s[i-1] ;
     cin >> s ;
     fi( i , 1 , n ) b[i] = s[i-1] ;

     fi( i , 1 , n/2 ){
          int l = i , r = n-i+1 ;
          ds.clear() ;
          ds.push_back(a[l]) ; ds.push_back(a[r]) ;
          ds.push_back(b[l]) ; ds.push_back(b[r]) ;

          Solve( l , r ) ;
     }

     if ( n%2==1 )
          if ( a[n/2+1] != b[n/2+1] )
               ans++ ;

     cout << ans ;

}