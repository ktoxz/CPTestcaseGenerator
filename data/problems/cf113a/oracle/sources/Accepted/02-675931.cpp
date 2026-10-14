#include<stdio.h>
#include<iostream>
#include<string>
#include<algorithm>
using namespace std;
bool g[5];
string str[100003];
int f(string a)
{
    reverse(a.begin(),a.end());
    if (a.length()>=4&&a.substr(0,4)=="soil") return 1;
    if (a.length()>=5&&a.substr(0,5)=="alail") return 2;
    if (a.length()>=3&&a.substr(0,3)=="rte") return 3;
    if (a.length()>=4&&a.substr(0,4)=="arte") return 4;
    if (a.length()>=6&&a.substr(0,6)=="sitini") return 5;
    if (a.length()>=6&&a.substr(0,6)=="setini") return 6;
}
int main()
{
    //freopen("in.txt","r",stdin);
    int c1,i,j,k;
    bool d;
    c1=0;
    while (cin>>str[c1]) c1++;
    if (c1==1&&(f(str[0])==1||f(str[0])==2||f(str[0])==3||f(str[0])==4||f(str[0])==5||f(str[0])==6)) printf("YES\n");
    else
    {
        d=0;
        for (i=0;i<c1;i++)
        {
            if (f(str[i])==1) g[1]=1;
            else if (f(str[i])==2) g[2]=1;
            else break;
        }
        if (i<c1&&f(str[i])==-1) d=1;
        if (g[1]&&g[2]) d=1;
        for (j=i;j<c1;j++)
        {
            if (f(str[j])==3) g[1]=1;
            else if (f(str[j])==4) g[2]=1;
            else break;
        }
        if (j<c1&&f(str[j])==-1) d=1;
        if (g[1]&&g[2]) d=1;
        if (j-i!=1) d=1;
        for (k=j;k<c1;k++)
        {
            if (f(str[k])==5) g[1]=1;
            else if (f(str[k])==6) g[2]=1;
            else break;
        }
        if (k<c1&&f(str[k])==-1) d=1;
        if (g[1]&&g[2]) d=1;
        if (k<c1) d=1;
        if (!d) printf("YES\n");
        else printf("NO\n");
    }
    return 0;
}