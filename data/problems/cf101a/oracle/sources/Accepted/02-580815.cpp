#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <queue>
#include <functional>
using namespace std;
#define N 100010
struct node
{
    char name;
    int num;
};
node le[26];
char ch[N];
bool flag[26];
int len;
int sum;
int k;
bool cmp(const node x,const node y)
{
    if(x.num<y.num)
    return true;
    else
    return false;
}
int main()
{
    for(int i=0;i<26;i++)
    {
        le[i].name=i+'a';
        le[i].num=0;
    }
    scanf("%s",ch);
    scanf("%d",&k);
    len=strlen(ch);
    for(int i=0;i<len;i++)
    le[ch[i]-'a'].num++;
    sort(le,le+26,cmp);
    sum=0;
    for(int i=0;i<26;i++)
    {
        if(le[i].num!=0)
        sum++;
    }
    for(int i=0;i<26;i++)
    {
        if(le[i].num==0) continue;
        k-=le[i].num;
        if(k<0) break;
        if(k>=0)
        {
            sum--;
            le[i].num=0;
        }
    }
    for(int i=0;i<26;i++)
    if(le[i].num!=0)
    flag[le[i].name-'a']=1;
    printf("%d\n",sum);
    if(sum>0)
    {
        for(int i=0;i<len;i++)
        {
            if(flag[ch[i]-'a']==1)
            printf("%c",ch[i]);
        }
        printf("\n");
    }
    return 0;
}