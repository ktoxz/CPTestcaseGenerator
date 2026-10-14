#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

int main()
{
    int n,k,m,ans=0;
    int p[5000];
    cin >> n;
    for (int i=0; i<n; i++) {
        cin >> p[i];
        if (p[i]!=-1)
            p[i]--;
    }
    for (int i=0; i<n; i++) {
        k = i;
        m = 0;
        while (k!=-1) {
            k = p[k];
            m++;
        }
        if (m>=ans)
            ans = m;
    }
    cout << ans;
}