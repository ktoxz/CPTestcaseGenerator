#include<stdio.h>

#include<stdlib.h>

#include<string.h>

long long result(long long n,long long m)

{

     if(n<m)

     return 0;

     int i,t=1,ans=1;

     for(i=n;i>m;i--)/*Computation of the combination aCb*/

     {

          ans*=i;

          ans/=t++;

     }

     return ans;

}

char* bitchange(char* ch)

{

     int i,t=0,cnt=0,j,k=0;

     t=strlen(ch);

     for(i=t-1;i>=0;i--)

     {

          if(ch[i]=='1')

          cnt++;

          else

          {

               k=i;

               break;

          }

     }

   //  printf("%d %s\n",cnt,ch);

     if(cnt==t)

     {

          ch[0]='1';

          ch[t]='0';

          ch[t+1]='\0';

          k=1;

     }

     for(i=k;i<t;i++)

     {

          if(ch[i]=='1')

          ch[i]='0';

          else if(ch[i]=='0')

          ch[i]='1';

        //  printf("c== %d",ch[i]);

     }

     if(cnt!=t)

     ch[t]='\0';

     //printf("\n%d %s\n\n",t,ch);

     return ch;

}

int cmpfunc(const void*a,const void*b)

{

    return (*(int*)a - *(int*)b);

}

int main()

{

    int n,m,i,j,sum=1,chk=0,z=0,k=0,t=0,s=0,max=0,min=0,d=0;

    int a[2000005]={0},b[5000]={0},c[1000001]={0},y[1000001]={0};

    scanf("%d %d",&n,&d);

    for(i=1;i<=n;i++)

    {

         scanf("%d",&a[i]);

         if(i>1)

         {

              if(a[i]<=a[i-1])

              {

                   t=(a[i-1]-a[i])/d;

                   t++;

                   sum+=t;

                   a[i]+=(t*d);

                   

              }

         }

    }

    printf("%d",sum-1);

    return 0;

    

    

}