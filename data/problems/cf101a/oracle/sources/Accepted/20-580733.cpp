#include<stdio.h>
#include<string.h>
char s[200000];
long f[100];
long c[100];
long p[100];
long l,i,k,j,kk,temp,ans;
int main()
{
    scanf("%s",s);
    scanf("%d",&kk);
    l=strlen(s)-1;
    for (i=0;i<=l;i++)
    {
        c[s[i]-96]++;
    }
    for (i=1;i<=26;i++)
    {
      p[i]=i;
      f[i]=i;
    }
  for (k=1;k<=25;k++)
      for (i=25;i>=1;i--)
    {
        j=i+1;
        if (c[i]>c[j])
        {
            temp=c[i];
            c[i]=c[j];
            c[j]=temp;
            temp=p[f[i]];
            p[f[i]]=p[f[j]];
            p[f[j]]=temp;
            temp=f[i];
            f[i]=f[j];
            f[j]=temp;
        }
    }
  for (i=1;i<=26;i++)
  {
    if (c[i]<=kk)
    {
        kk-=c[i];
        c[i]=0;
      }
      else if (c[i]>kk)
      {
        c[i]-=kk;
        kk=0;
    }
    if (kk==0)
      break;
  }
  ans=0;
  for (i=1;i<=26;i++)
  {
    if (c[i]>0)
      ans++;
  }
  printf("%d\n",ans);
    for (i=0;i<=l;i++)
    {
        if (c[p[s[i]-96]]>0)
        {
            printf("%c",s[i]);
            c[p[s[i]-96]]--;
        }
    }
}