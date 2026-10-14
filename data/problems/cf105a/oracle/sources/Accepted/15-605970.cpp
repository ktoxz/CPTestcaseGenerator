/*****************************************
*
* 2011,UESTC_ACM
* Transmigration
* By a180285
*
*****************************************/

# include <math.h>
# include <stdio.h>
# include <string.h>
# include <stdlib.h>
# include <algorithm>
# include <iostream>
# include <string>
# include <queue>
# include <stack>
# include <map>
# include <set>
# include <vector>
# include <cstring>
# include <list>
# include <ctime>
# include <sstream>

# define For(i,a)   for((i)=0;i<(a);(i)++)
# define MAX(x,y)   ((x)>(y)? (x):(y))
# define MIN(x,y)   ((x)<(y)? (x):(y))
# define sz(a)      (sizeof(a))
# define MEM(a)     (memset((a),0,sizeof(a)))
# define MEME(a)    (memset((a),-1,sizeof(a)))
# define MEMX(a)    (memset((a),0x7f,sizeof(a)))
# define pb(a)      push_back(a)

using namespace std;

typedef long long           ll      ;
typedef unsigned long long  ull     ;
typedef unsigned int        uint    ;
typedef unsigned char       uchar   ;


template<class T> inline void checkmin(T &a,T b){if(a>b) a=b;}
template<class T> inline void checkmax(T &a,T b){if(a<b) a=b;}

const int oo=1<<30          ;
const double eps=1e-7       ;
const int N=1               ;
const int M=1               ;
const ll P=10000000097ll    ;

int up;
map<string,int> mp;
map<string,int>::iterator it;

void in(int n)
{
    string s;
    int tp;
    int i,j,k;
    For(i, n)
    {
        cin >> s >> tp;
        tp = tp*up/100;
        if( tp >= 100 )
        {
            mp[s] = tp;
        }
    }
}

void in_(int n)
{
    string s;
    int i,j,k;
    For(i, n)
    {
        cin >> s;
        mp[s] ;
    }
}

int main()
{
    int T,_=0;
    int n,m;
    int i,j,k;
    double x;
    scanf("%d %d %lf", &n, &m, &x);
    up = x*100 + 0.5;
    in(n);
    in_(m);

    n = mp.size();
    printf("%d\n",n);
    for(it=mp.begin(); it!=mp.end(); it++)
    {
        cout << it->first << " " << it->second << endl;
    }
    return 0;
}

/**

input
5 4 0.75
axe 350
impaler 300
ionize 80
megafire 120
magicboost 220
heal
megafire
shield
magicboost
output
6
axe 262
heal 0
impaler 225
magicboost 165
megafire 0
shield 0

**/