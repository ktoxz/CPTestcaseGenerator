#include <map>

#include <iostream>

#include <algorithm>

#include <stdlib.h>

#include <stdio.h>

#include <string.h>

#include <cmath>

#include <cstdio>

#include <vector>

#include <queue>

#include <stack>

#include <sstream>

#include <fstream>

#include <iomanip>

#define PI acos(-1.0);

using namespace std;

typedef long long ll;

typedef vector<ll> vi;





int main() {

    ios_base::sync_with_stdio(0);

    ll n,k;

    cin>>n>>k;

    ll count=0;

    ll c = n;

    while (c<=k) {

        if (c==k) {

            cout<<"YES\n";

            cout<<count;

            return 0;

        }

        count++;

        c*=n;

    }

    cout<<"NO";

    return 0;

}