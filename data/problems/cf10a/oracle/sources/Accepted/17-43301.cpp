/******************\
*    CPP source    *
*     By HPFDF     *
\******************/
#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdlib>
#include <iomanip>
#include <cstdio>
#include <string>
#include <cmath>
#include <ctime>
#include <algorithm>
#include <complex>
#include <vector>
#include <map>
#include <set>
#define rep(i,n)   for(int i=0;i<(n);++i)
#define fab(i,a,b) for(int i=(a);i<=(b);++i)
#define fba(i,b,a) for(int i=(b);i>=(a);--i)
#define fec(i,a)   for(typeof(a.end())i=a.begin();i!=a.end();++i)
#define fpc(i,v)   for(int i=a[v];i;i=nx[v])
#define fil(a)     memset(a,0,sizeof(a))
#define all(a)     a.begin(),a.end()
#define rdm        srand(time(NULL))
using namespace std;
const int HX = 0x3F3F3F3F;
/****************************\
*            MAIN            *
\****************************/

int n, m, k, p1, p2, p3, t1, t2, l, r, l1, rn;
int f[2000];
int main()
{
    cin >> n >> p1 >> p2 >> p3 >> t1 >> t2;
    k = 0;
    m = 0;
    long long ans = 0;
    rep(i, n)
    {
        cin >> l >> r;
        if (i == 0) l1 = l;
        rn = r;
        fab(j, l, r) f[j] = 1;
    }
    fab(i, l1, rn - 1)
    {
        if (f[i] == 1) f[i] = 0, ans += p1; else
        {
            f[i] = f[i - 1] + 1;
            if (f[i] < t1)
                ans += p1; else
            if (f[i] < t1 + t2)
                ans += p2; else
                ans += p3;
        }
    }
    cout << ans << endl;
    return 0;
}


/****************************\
*            EOF             *
\****************************/