#include <bits/stdc++.h>

using namespace std;

long long z[1000005];

int main()

{

    //freopen("cin.txt","r",stdin);

    int n,a,d,count,i;

    long long x;

    count=0;

    cin>>n>>d;

    for(a=0;n>a;a++){

        cin>>z[a];

    }

    for(a=1;n>a;a++){

        i=0;

        if(z[a]<=z[a-1]){

            x=z[a-1]-z[a];

            //cout<<z[a-1]<<z[a]<<endl;

            if(x<d){

                //cout<<"z";

                i++;

            }

            else{

                i++;

                i+=x/d;

            }

            z[a]+=i*d;

            //cout<<i<<d<<z[a];

        }

        count+=i;

        //cout<<z[a]<<endl;

    }

    cout<<count<<endl;

    return 0;

}