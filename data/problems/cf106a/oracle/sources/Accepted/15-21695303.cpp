#include <iostream>

#include <string>

#include <stdio.h>

#include <algorithm>

#include <cmath>

#include <math.h>

#include <set>

#include <vector>

#include <map>

#include <queue>

#include <stack>

#include <sstream>

#include <iomanip>

#include <cstdio>

#include <list>

#include <fstream>

#define ull unsigned long long

#define ll long long

#define ld long double

#define pi 3.1415926536

#define lp(i,n,a) for(ll i=a;i<=n;i++)

#define pl(i,n) for(ll i=n-1;i>=0;i--)

#define w while

#define re return

using namespace std;

char a,b,c,x,y;

map<char,int> m;

int main() {

	ios_base::sync_with_stdio(0);

	cin.tie(0);cout.tie(0);

        cin >> a >> b >> c >> x >> y;

        m['6']=1;

        m['7']=2;

        m['8']=3;

        m['9']=4;

        m['T']=5;

        m['J']=6;

        m['Q']=7;

        m['K']=8;

        m['A']=9;

        if(a!=y && a==c){

             cout << "YES";

             re 0;

        }

        if(c==y && m[b]>m[x]){

              cout << "YES";

              re 0;

        }

        cout << "NO";

re 0;

}