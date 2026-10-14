#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef unsigned long long ull;
typedef long double ldouble;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int n,ans = 0, el; cin >> n;
    multiset <int> q;
    vector <int> p = {1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824};
    for (int i = 0; i < n; i++) {
        cin >> el;
        q.insert(el);
    }
    
    for (multiset<int>::iterator it = q.begin(); it != q.end(); it++) {
        bool res = false;
        for (int j = 0; j < p.size(); j++) {
            if (p[j] > *it) {
                auto m = q.find(p[j] - *it);
                if (m != q.end() && (m != it || q.count(p[j] - *it) > 1)) {res = true; break;}
            }
        }
        if (!res) ans++;
    }
    
    cout << ans;
    
    return 0;
}