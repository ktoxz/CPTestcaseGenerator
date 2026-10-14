#include <iostream>

#include <string>

#include <set>

#include <map>

#include <stack>

#include <queue>

#include <vector>

#include <utility>

#include <iomanip>

#include <sstream>

#include <bitset>

#include <cstdlib>

#include <iterator>

#include <algorithm>

#include <cstdio>

#include <cctype>

#include <cmath>

#include <math.h>

#include <ctime>

#include <cstring>

using namespace std;

#define cos(a) cos(a*pi/180)

#define sin(a) sin(a*pi/180)

#define tan(a) tan(a*pi/180)

#define cosi(a) acos(a)/(pi/180)

#define sini(a) asin(a)/(pi/180)

#define tani(a) atan(a)/(pi/180)



///IO AND FORLOOP

#define f1(i,n) for(int i = 1; i <= (int)(n); i++) //1 BASED

#define f0(i,n) for(int i = 0; i < (int)(n); i++)  //0 BASED

#define fr1(i, n) for(int i = (int)(n) ; i >= 1; i--) //1 BASED REVERSE

#define fr0(i, n) for(int i = (int)(n) ; i > 0; i--) //0 BASED REVERSE

#define fast_cin ios_base::sync_with_stdio(false);cin.tie(NULL)

#define sf      scanf

#define pf      printf

#define si(a) int a; scanf("%d", &a);

#define sll(a) ll a; scanf("%lld", &a);

#define sllu(a) unsigned ll a; scanf("%llu", &a);

#define sd(a) double a; scanf("%lf", &a);

#define pi(a) printf("%d", a);

#define pll(a) printf("%lld", a);

#define pllu(a) printf("%llu", a);

#define pd(a) printf("%lf", a);

#define pb push_back;

#define rv(a) reverse(a.begin(),a.end());

const double pi=2*acos(0);

typedef string st;

typedef vector <int> vi;

typedef vector <string> vs;

typedef pair <int, int> ii;

typedef long long ll;

typedef vector < pair <int, int> > vii;

typedef priority_queue<int,vector<int>,greater<int> > min_heap;

using namespace std;

int main(void)

{

   fast_cin;

   st a[100],b[100];

    f1(i,3)

    {

        cin>>a[i];

        b[i]=a[i];

        rv(b[i]);

    }

    for(int i=1,j=3;i<=3;i++,j--)

    {

        if(a[i]!=b[j])

        {

            cout<<"NO"<<endl;

            return 0;

        }



    }

    cout<<"YES"<<endl;



}