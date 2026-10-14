#include<stdio.h>

#include<string.h>

#include<stdlib.h>

#define ll long long

#define N 300005

int a[N];

int main()

{

     int i,t,n;

     char n1[N],n2[N],temp[N];

     scanf("%s",n1);

     getchar();

     scanf("%s",n2);

     getchar();

     if(n1[0]==n2[0]&&(strlen(n1)==strlen(n2))&&(strlen(n1)==1))

     {

          puts("OK");

          return 0;

     }

     if(n2[0]=='0')

     {

          puts("WRONG_ANSWER");

          return 0;

     }

     for(i=0;n1[i];i++)

     {

          a[n1[i]]++;

     }

     t=a[48];

     for(i=49;i<=57;i++)

     {

          if(a[i])

          {

               n=a[i];

               break;

          }

     }

     if(t);

     {

          for(i=1;i<t+1;i++)

          {

               temp[i]=48;

          }

     }

     int j=0;

     for(i=49;i<=57;i++)

     {

          while(a[i]--)

          {temp[j]=i;

          j++;

          if(t&&j==1)

          j=1+t;

          }

     }

     temp[j]='\0';

     //puts(temp);

     if(strcmp(temp,n2)==0)

     puts("OK");

     else

     puts("WRONG_ANSWER");

     return 0;

}