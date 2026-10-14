#include<stdio.h>

int c=1;

int gcd(int m,int n);

int main()

{

    int a,b,k,p,q;

    scanf("%d%d%d",&a,&b,&k);

    while(1)

    {

        if(c%2==1)

        {

            p=gcd(a,k);

            k=k-p;

            if(k==0)

            {

                if(c%2==0)

                {

                    printf("0\n");

                }

                else

                {

                    printf("1\n");

                }

                 return 0;

            }

        }

        if(c%2==0)

        {

            q=gcd(b,k);

            k=k-q;

            if(k==0)

            {

                if(c%2==0)

                {

                    printf("0\n");

                }

                else

                {

                    printf("1\n");

                }

                  return 0;

            }

        }



    }

}

int gcd(int m,int n)

{

    int i,temp,gcd1;

    if(m<n)

    {

        temp=m;

        m=n;

        n=temp;

    }

    for(i=1; i<=n; i++)

    {

        if(m%i==0 && n%i==0)

            gcd1=i;

    }

    c++;

    return gcd1;

}