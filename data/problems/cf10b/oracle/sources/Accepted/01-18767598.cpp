#include<bits/stdc++.h>

using namespace std;

int a[101][101];

int dp[101][101];

int c,f,n,m,z,x,y,mc,q,qq;

int dis(int i,int j){return abs(i-c)+abs(j-c);}

int main()

{

cin>>n>>m;

c=(m+1)/2;

for(int i=1;i<=m;i++)

for(int j=1;j<=m;j++)

a[i][j]=j,dp[i][j]+=dp[i][j-1]+dis(i,j);

for(int ix=0;ix<n;ix++)

{

cin>>z;f=-1;

for(int i=1;i<=m;i++)for(int j=1;j<=m;j++)

{



 x=a[i][j+z-1]-a[i][j-1];

 y=dp[i][j+z-1]-dp[i][j-1];



 if(x==z&&(f==-1||y<mc))

 {

     mc=y;f=i;q=j;

 }

}



if(f==-1){cout<<"-1"<<endl;}

else{

    cout<<f<<" "<<q<<" "<< q+z-1<<endl;

    for(int iii=q;iii<=m;iii++)a[f][iii]-=min(z,iii-q+1);

}



}//eof

return 0;

}