#include<stdio.h>
#include<iostream>
#include<algorithm>
#include<string>
using namespace std;

string a,b;
int n;
int kq;

void process(char a,char b,char c,char d){
  if (a==b){
    if (c==d) kq=kq+0;
    else{
      if (a==c || a==d) kq=kq+1;
      else kq=kq+2;
    }
  }
  else{
    if (c==d) kq=kq+1;
    else{
      int z[]={a,b,c,d};
      sort(z+0,z+4);int t=1;
      for(int i=1;i<=3;i++)
        if (z[i-1]!=z[i]) t++;
      if (t==4) kq=kq+2;
      if (t==3) kq=kq+1;
    }
  }
}

int main(){
  //freopen("input.txt","r",stdin);
  scanf("%d",&n);
  cin>>a;cin>>b;
  kq=0;
  for(int i=0;i<=(n-1)/2;i++){
    if (i!=n-1-i) process(a[i],a[n-1-i],b[i],b[n-1-i]);
    else
      if (a[i]!=b[i]) kq++;
    //printf("i=%d Kq=%d\n",i,kq);
  }
  printf("%d",kq);
}