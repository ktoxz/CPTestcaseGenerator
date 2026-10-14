#include<iostream>
#include<stdio.h>
#include<vector>
#include<cmath>
#include<queue>
#include<string.h>
#include<map>
#include<iomanip>
#include<algorithm>
#define ll long long
#define rep(i,a,b) for(int i = a;i < b;i++)
#define N 100004
#define INF 1e9+7
#define EPS 1e-8

using namespace std;

ll n;
double m;
double a[N],b[N];

bool check(double olo)
{
    double fuel = olo;

    rep(i,0,n)
    {
        fuel -= (m + fuel)/(a[i]);

        fuel -= (m + fuel)/(b[i]);
    }

    return fuel >= 0;
}

int main()
{
    ios_base::sync_with_stdio(false);

    cin >> n >> m;

    rep(i,0,n)
    {
        cin >> a[i];
    }

    rep(i,0,n)
    {
        cin >> b[i];
    }

    double low = 0;
    double high = INF;

    while(high - low >= 0.0000001)
    {
        double mid = (low + high)/2;

        if(check(mid))
        {
            high = mid;
        }
        else
        {
            low = mid;
        }
    }

    if(low > 1e9)
    {
        cout << -1 << endl;
        return 0;
    }

    cout << fixed << setprecision(10) << low << endl;

    return 0;
}