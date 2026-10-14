#include<cstdio>

#include<algorithm>

#include<iostream>

#include<cmath>

#include<cstdlib>

#include<map>

#include<bits/stdc++.h>

#define ll long long

#define sl(x) scanf("%d",&x)

#define sll(x,y) scanf("%d%d",&x,&y)

#define slll(x,y,z) scanf("%d%d%d",&x,&y,&z)

#define ms(x,y) memset(x,y,sizeof(x))

#define fori(x) for(int i=0;i<x;i++)

#define forj(x) for(int j=0;j<x;j++)

#define prt(x) printf("%d\n",x)

#define N 200000+5

#define INF 2147483646;

using namespace std;

double a,b,gcd,n1,n2,n3,n4,cnt1,cnt2,maxi,mini,cnt,ans1,ans2,n,x[N],room,p;

double tmp1,tmp2;



double c(double tp1,double tp2,double down){

    double ret=1;

    fori(down){

        ret*=(tp1-i)/(tp2-i);

    }

    return ret;

}



int main(){



    cin>>n>>room>>p;

    double sum=0;

    fori(room){

        cin>>x[i];

        if(i==p-1) a=x[i];

        sum+=x[i];

    }

    double ans=c(sum-a,sum-1,n-1);

    if(sum<n) prt(-1);

    else printf("%.7f\n",1-ans);



}