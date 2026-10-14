#include <bits/stdc++.h>



#define ll long long

#define oo 1e18



const int N = 1e2 + 1;



using namespace std;



int n, r[N], d[N], s[N], p[N];



int main()

{

    //freopen("input.txt", "r", stdin);

    std :: ios :: sync_with_stdio (false);

    cin >> n;

    for (int i = 0; i < n; i++)

        cin >> s[i] >> r[i] >> d[i] >> p[i];

    int it, ans = 1001;

    for (int i = 0; i < n; i++)

    {

        bool ok = true;

        for (int j = 0; j < n; j++)

        {

            if (j == i) continue;

            if (s[i] < s[j] && d[i] < d[j] && r[i] < r[j])

            {

                ok = false;

                break;

            }

        }

        if (ok && p[i] < ans)

            ans = p[i], it = i;

    }

    cout << it + 1;

    return 0;

}