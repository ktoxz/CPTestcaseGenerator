#include<bits/stdc++.h>



    using namespace std;

    typedef long long ll;



    string To_string(int a);

    int gcd (int x,int y);

    int find_min(int a[],int n);

    int find_max(int a[],int n);





    int main()

    {

        int a,b,c;

        cin>>a>>b>>c;



        while(1)

        {

            if(gcd(a,c)>c)

            {

                cout<<1;

                return 0;

            }

            else

                c-=gcd(a,c);



            if(gcd(b,c)>c)

            {

                cout<<0;

                return 0;

            }

            else

                c-=gcd(b,c);









        }







        return 0;

    }





    string To_string(int a)

    {

        string s="";

        while(a)

        {

            s+=(a%10+'0');

            a/=10;

        }

        reverse(s.begin(),s.end());

        return s;

    }



    int gcd (int x,int y)

    {

        if(x==0)

            return y;

        if(y==0)

            return x;



        if(x==y)

            return x;

        else

        {

            if(x>y)

                return gcd (x-y,y);

            else

                return gcd (x,y-x);

        }



    }



    int find_min(int a[],int n)

    {

        int b=a[0];

        int k=0;

        for(int i=1;i<n;i++)

        {

            if(a[i]<b)

            {

                b=a[i];

                k=i;

            }



        }

        return k+1;





    }



    int find_max(int a[],int n)

    {

        int b=a[0];

        int k=0;

        for(int i=1;i<n;i++)

        {

            if(a[i]>b)

            {

                b=a[i];

                k=i;

            }



        }

        return k+1;





    }