#include <bits/stdc++.h>

#include <fstream>



typedef long long ll;

typedef unsigned long long ull;

typedef long double ld;



using namespace std;



double Fib(double x,double z);

string BinDec(ull x);

string StringInt(ll x);

ull StringInt(string x);

ull BinDec (string x);

ull POWMOD (ull x,ull y,ull mod);

ull POWE(long long , long long);





int main()

{



    ios::sync_with_stdio(false);

    cin.tie(0);

    int n,i,j,y[200]={},z[200]={},a[200]={},x[200]={},c[200]={};

    cin>>n;

    for(i=0;i<n;i++)

    {

        cin>>x[i]>>y[i]>>z[i]>>a[i];

    }

    for(i=0;i<n;i++)

    {

        for(j=0;j<n;j++)

        {

            if(i==j)continue;

            if(x[i]<x[j]&&y[i]<y[j]&&z[i]<z[j])

            {

                c[i]=1;

                break;

            }

        }

    }

    int ans=10000,k;

    for(i=0;i<n;i++)

    {

        if(c[i]==1)continue;

        if(ans>a[i])

        {

            ans=a[i];

            k=i;

        }

    }

    cout<<k+1;





    return 0;

}



double Fib(double x,double z){

    int i=0;

    double f=x,r=x,t;

    for(i=2;i<z;i++)

    {

        t=f;

        f+=r;

        r=t;

    }

    return f;



}

string BinDec( ull x){

    string z;

    while(1)

    {

        z+=((x%3)+'0');

        x/=3;

        if(x==0)

            break;

    }

    while(1)

    {

        if(z.size()==30)

            break;

        z+='0';

    }

    reverse(z.begin(),z.end());

    return z;

}

ull BinDec(string x){

    long long i;

    unsigned long long z=1,a=0;

    for(i=x.size()-1;i>=0;i--)

    {

        if(x[i]=='1')

            a+=z;

        if(x[i]=='2')

            a+=(2*z);

        z*=3;

    }

    return a;

}

ull StringInt(string x){

   ull z=0,i;

   for(i=0;i<x.size();i++)

   {

       z*=10;

       z+=(x[i]-'0');

   }

   return z;

}

string StringInt(ll x){

    string z;

    while(x!=0)

    {

        z+=(x%10+'0');

        x/=10;

    }

    reverse(z.begin(),z.end());

    return z;

}

ull POWMOD (ull base,ull exp,ull mod){

    ull res=1;

    while(exp>0){

        if(exp%2==1)

            res=(res*base);

            res%=mod;

        exp/=2;

        base=(base*base);

        base%=mod;

    }

return res%mod;

}

ull POWE(long long base,long long exp){

    ull res=1;

    while(exp>0){

        if(exp%2==1)

            res=(res*base);

        exp/=2;

        base=(base*base);

    }

return res;



}



/*

int s=0,c[1553][1553]={},z;

char a[1550][1550]={};

void lol(char m,int i,int j,int & s)

{



    if(c[i][j+1]==0&&a[i][j+1]==m)

    {

        s++;

        c[i][j+1]=1;

        lol(m,i,j+1,s);

    }

    if(c[i][j-1]==0&&a[i][j-1]==m)

    {

        s++;

        c[i][j-1]=1;

        lol(m,i,j-1,s);

    }

    if(c[i-1][j]==0&&a[i-1][j]==m)

    {

        s++;

        c[i-1][j]=1;

        lol(m,i-1,j,s);

    }

    if(c[i+1][j]==0&&a[i+1][j]==m)

    {

        s++;

        c[i+1][j]=1;

        lol(m,i+1,j,s);

    }

    if(z!=0)

    {

        z--;

        a[i][j]='X';

    }

    return;

}*/