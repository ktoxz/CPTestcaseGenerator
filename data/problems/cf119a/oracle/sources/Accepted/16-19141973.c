#include<stdio.h>

int main()

{

    int a,b,n,kq,dem=0;

    scanf("%d%d%d",&a,&b,&n);

    for (int i=1;;i++)

    {

        if (i%2!=0)

        {

            if (n>=a)

            {

                if (n%a==0)

                {

                    n=n-a;

                    if (n==0)

                    {

                    printf("0");break;

                    }

                }

                else

                {

                    n=n-1;

                    if (n==0)

                    {

                    printf("0");break;

                    }

                }

            }

            else

            {

                if (n<a)

                {

                    if (a%n==0)

                    {

                        printf("0");break;

                    }

                    else

                    {

                        n=n-1;

                        if (n==0)

                        {

                            printf("0");break;

                        }

                    }

                }

            }

        }

        else

        {

            if (n>=b)

            {

                if (n%b==0)

                {

                    n=n-b;

                    if (n==0)

                    {

                    printf("1");break;

                    }

                }

                else

                {

                    n=n-1;

                    if (n==0)

                    {

                    printf("1");break;

                    }

                }

            }

            else

            {

                if (n<b)

                {

                    if (b%n==0)

                    {

                        printf("1");break;

                    }

                    else

                    {

                        n=n-1;

                        if (n==0)

                        {

                            printf("1");break;

                        }

                    }

                }

            }

        }

    }

}