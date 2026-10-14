#include<string>
#include<iostream>
#include<sstream>
#include<assert.h>
#include<cstdio>
#include<map>
#include<algorithm>
#include<bitset>
#include<cmath>
#include<queue>
#include<functional>
#include<set>
#include<stack>
#include<cstdlib>
#include<cstring>


using namespace std;

//=========================================================
// program:
//
long B[2000];

long solve(int n, int d) {
    long t = 0;
    for (int i=1; i<n; i++) {
        if( B[i] <= B[i-1] ) {
            long bottom = 0;
            long x = 10000000;
            while ( bottom+1 != x ) {
                long ha = (bottom+x)/2;
                if ( (d > B[i-1]/ha) || ( B[i] > B[i-1]-d*ha ) ) {
                    x = ha;
                } else {
                    bottom = ha;
                }
            }
            B[i] += x * d;
            t += x;
        }
    }
    return t;
}
inline void init(){}
//=========================================================
// I/O:
//
int main()
{
    init();
    //int C; cin>>C;
    int n,d;
    
    while( cin >> n >> d)
    {
        for (int i=0; i<n; i++) {
            cin >> B[i];
        }
        cout << solve(n,d) << endl;
        
    }
    return 0;
}