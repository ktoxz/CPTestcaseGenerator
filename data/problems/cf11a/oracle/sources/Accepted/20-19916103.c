#include<stdio.h>

int main ()

{

    int a[2000],n,d,count=0,i;

    scanf("%d %d",&n,&d);

    for(i=0;i<n;i++)

    {

        scanf("%d",&a[i]);

        if(i>0)

        {

            if(a[i]<=a[i-1])

            {

                if(a[i]==a[i-1])a[i]=a[i]+d,count++/*printf("%d %d\n",i+1,count)*/;

                else

                {

                    int substract=a[i-1]-a[i];

                    int devider=substract/d;

                    a[i]=a[i]+((devider+1)*d),count=count+devider+1;

                    //printf("%d %d\n",i+1,count);

                }

            }

        }

    }

    //for(i=0;i<n;i++)printf("%d ",a[i]);

    //printf("\n");

    printf("%d\n",count);

    return 0;

}