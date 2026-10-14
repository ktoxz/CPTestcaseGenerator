#include <bits/stdc++.h>

using namespace std;

int gcd(int a,int b)

{

    if(b==0)

        return a;

    return (gcd(b,a%b));

}

int main()

{

    int a,b,n,flag=0,tmp;

    cin>>a>>b>>n;

    while(n>0)

    {

        if(flag%2==0)

        {

            tmp = gcd(a,n);

            if(tmp<=n)

            {

                n-=tmp;

                flag++;

            }

        }

        else

        {

            tmp = gcd(b,n);

            if(tmp<=n)

            {

                n-=tmp;

                flag++;

            }

        }

    }

    if(flag%2==0)

        cout<<1;

    else

        cout<<0;

    return 0;

}