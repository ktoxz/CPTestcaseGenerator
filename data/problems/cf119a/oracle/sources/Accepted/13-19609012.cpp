#include <bits/stdc++.h>

using namespace std;

int main()

{

    int a,b,n;

    cin >> a >> b >> n;

    int ans=0;

    while (n!=0)

    {

        if (ans%2==0)

        {

            n=n-__gcd(n,a);

        }

        else

        {

            n=n-__gcd(n,b);

        }

        ans++;

    }

    if (ans%2)

    {

        cout << 0 << endl;

    }

    else

    {

        cout << 1 << endl;

    }

    return 0;

}