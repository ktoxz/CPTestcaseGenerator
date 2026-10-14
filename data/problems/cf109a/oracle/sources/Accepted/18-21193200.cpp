#include <bits/stdc++.h>

using namespace std;

typedef long long ll;



int main()

{

    ios_base::sync_with_stdio(0);

    cin.tie(0);

    int n,m,k;

    cin>>n;

    for (int i=0;i<=n;i++)

    {

        if ((n-(4*i))>=0&&(n-(4*i))%7==0)

        {

            for (int j=0;j<i;j++)

                cout<<"4";

            for (int j=0;j<(n-(4*i))/7;j++)

                cout<<"7";

            cout<<endl;

            return 0;

        }

    }

    cout<<-1<<endl;

    return 0;

}