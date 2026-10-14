#include <bits/stdc++.h>



using namespace std;



#define ios        ios_base::sync_with_stdio(false); cin.tie(false); cout.tie(false);

#define eps 1e-9



template< class T > T _abs(T n) { return (n < 0 ? -n : n); }

template< class T > T _max(T a, T b) { return (!(a < b) ? a : b); }

template< class T > T _min(T a, T b) { return (a < b ? a : b); }

template< class T > T sq(T x) { return x * x; }

template< class T > T gcd(T a, T b) { return (b != 0 ? gcd<T>(b, a%b) : a); }

template< class T > T lcm(T a, T b) { return (a / gcd<T>(a, b) * b); }

template < class T > T power(T N , T P) { return (P == 0) ?  1 : N * power(N , P - 1); }





typedef long long ll ;





/// S , E  , N , W

int rr [] = {1 ,0,-1, 0};

int cc [] = {0 ,1, 0,-1};

///S , SE , E , NE , N , NW , W , SW

//int rr [] = {1 ,1 ,0,-1,-1,-1, 0, 1};

//int cc [] = {0 ,1 ,1 ,1, 0,-1,-1,-1};

///Knight Direction

//int rr[]={2 ,1 ,-1,-2,-2,-1, 1, 2};

//int cc[]={1 ,2 , 2, 1,-1,-2,-2,-1};



//#define Maxi 65005



//bool siv[Maxi];

//ll sz = 0;

//ll prime[6709];

//ll cnt = 0 ;

//

//void is_prime()

//{

//    ll n = sqrt(Maxi);

//    prime[sz++] = 2;

//    for(ll i = 3 ; i < n ; i += 2) if(!siv[i]) for(ll j = i * i ; j < Maxi ; j += (2 * i)) siv[j] = true;

//    for(ll i = 3 ; i < Maxi ; i += 2) if(!siv[i])   prime[sz++] = i;

////    cout << prime[sz-1] << endl ;

////    cout << sz << endl ;

//}

//

//ll bigmod(ll num , ll p , ll mod)

//{

//    ll sum = 1 , temp = num;

//    while(p)

//    {

//        if(p & 1) sum = (sum * temp) % mod;

//        temp = (temp * temp) % mod; p = p >> 1;

//    }

//    return sum;

//}





int vis[110][110], cnt, R, C ;

char a[110][110], ch ;



//int bfs(int r, int c)

//{

//    queue < int > q ;

//    q.push(r) ;

//    q.push(c) ;

//    cnt = 1 ;

//    memset(vis, 0, sizeof vis) ;

//    vis[r][c] = 1 ;

//    while( !q.empty() )

//    {

//        int n, m, i, j, k ;

//        m = q.front(), q.pop() ;

//        n = q.front(), q.pop() ;

//        for( i = 0; i < 4; i++ )

//        {

//            j = m + rr[i] ;

//            k = n + cc[i] ;

//            if( k >= 0 && k < C && j >= 0 && j < R )

//            {

//                if( !vis[j][k] && a[j][k] == ch )

//                {

//                    vis[j][k] = 1 ;

//                    q.push(j) ;

//                    q.push(k) ;

//                    cnt++ ;

//                }

//            }

//        }

//    }

//    return cnt ;

//}



int main()

{

    int i, j, srt = 0 ;

    string a, b, c = "" ;

    char ch ;

    cin >> a >> b ;

    int memo[10] ;

    memset(memo, 0, sizeof memo) ;

    j = a.size() ;

    for( i = 0; i < j; i++ )

        memo[a[i]-'0']++ ;

    for( i = 1; i <= 9; i++ )

    {

        if( memo[i] )

        {

//            puts("hello") ;

            srt = i ;

            break ;

        }

    }

    int fl = 0 ;

    if( srt )

    {

        ch = srt + '0' ;

        c += ch ;

        memo[srt]-- ;

        for( i = 0; i <= 9; i++ )

        {

            for( j = 0; j < memo[i]; j++ )

            {

                ch = i + '0' ;

                c += ch ;

            }

        }

    }

    else

    {

        for( j = 0; j < memo[0]; j++ )

        {

            ch = 0 + '0' ;

            c += ch ;

        }

    }

//    cout << b << "  " << c << endl ;

    if( b == c )

        puts("OK") ;

    else

        puts("WRONG_ANSWER") ;



    return 0 ;

}