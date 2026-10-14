#include <bits/stdc++.h>

using namespace std;



int main(int argc, const char **argv) {

    if(argc>=2) {

        freopen(argv[1], "r", stdin);

        //freopen(argv[2], "w", stdout);

    }

    long long n, d;

    cin >> n >> d;

    vector<long long> a(n);

    for(int i=0 ; i< n ; i++) {

        scanf("%lld", &a[i]);

        //cerr<<i<<" "<<a[i]<<" "<<endl;

    }

    long long ans = 0;

    for(int i=1 ; i< n ; i++) {

        //cerr<<i<<" "<<a[i]<<" "<<a[i-1]<<" "<<endl;



        if (a[i] <= a[i-1]) {

            int b = a[i-1]-a[i];

            int c = 0;

            if (b % d) {

                c = 1;

            }

            b /= d;

            b += c;

            a[i] += b*d;

            if (a[i] == a[i-1]) {

                a[i]+=d;

                ans ++;

            }

            ans += b;

            //cerr<<i<<" "<<b<<" "<<c<<" "<<ans<<" " << a[i] << " " << a[i-1]<<endl;



        }

    }

    cout << ans << endl;

}