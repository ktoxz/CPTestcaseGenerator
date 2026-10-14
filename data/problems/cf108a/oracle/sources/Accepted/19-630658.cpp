#include <algorithm>
#include <bitset>
#include <cctype>
#include <cmath>
#include <complex>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <deque>
#include <fstream>
#include <iostream>
#include <list>
#include <map>
#include <memory>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <utility>
#include <vector>
#define REP(i,n) for(__typeof(n) i=0; i<(n); i++)
#define REP2(i,n) for(__typeof(n) i=1; i<=(n); i++)
#define FOR(i,a,b) for(__typeof(b) i=(a); i<=(b); i++)
#define INF (1<<30)
#define PI 3.14159265358979323846264338327950
#define PB(x) push_back(x)
#define ALL(x) x.begin(),x.end()
#define SZ size()
#define eps 1e-9
#define VI vector<int>
#define VS vector<string>
#define LL long long
#define MII map<int,int>
#define MSI map<string,int>
#define MIS map<int,string>
#define CLEAR(x) memset(x,0,sizeof(x));
#define MAX(a,b) (a>b?a:b)
#define MIN(a,b) (a<b?a:b)

using namespace std;
double area_triangle(double x1,double y1,double x2,double y2,double x3,double y3)
{
    double a;
    a=x1*(y2-y3)+y1*(x3-x2)+((x2*y3)-(y2*x3))+eps;
    a=a/2+eps;
return a;
}
double dist_2point(double x1,double y1,double x2,double y2)
{
    double d;
    d=sqrt(pow((x1-x2),2)+pow((y1-y2),2));
    return d;
}
int binary_search(int a[],int n,int l,int u)
{
    int mid;
  if(l>u)
      return 0;
  mid=floor(l+u)/2;
  if(a[mid]==n)
      return mid;
  else if(a[mid]>n)
      binary_search(a,n,l,mid-1);
      else
      binary_search(a,n,mid+1,u);
}
long  gcd(long a,long b)
{
if(a%b==0)
return b;
else
  gcd(b,a%b);
}
long lcm(long a,long b)
{
    long x=(a*b)/gcd(a,b);
    return x;
}
long is_prime(long n)
{
    long ii;
if (n == 1)
 return 0;
if (n == 2)
 return 1;
if (n%2 == 0)
 return 0;
for (ii=3;ii*ii<=n;ii=ii+2)
     if (n%ii == 0)
           return 0;
return 1;
}

int main()
{
char a[201]={0};
int i,j,h,m,h1,r,b;
//scanf("%d %c %d",&h,a[0],&m);
while(scanf("%s",a)!=EOF)
{
h=(a[0]-48)*10+a[1]-48;
m=(a[3]-48)*10+a[4]-48;
r=h%10;
b=h/10;
h1=r*10+b;
//printf("%d %d",h1,m);
/*if(m<h1&&h1<=60)
printf("%d:%d",h,h1);
else
{

    h=h+1;
    printf("%d:",h);
    r=h%10;
    b=h/10;
    h1=r*10+b;
    printf("%d\n",h1);
}*/
if(h<1)
printf("01:10\n");
else if(h==1&&m<10)
printf("01:10\n");

else if(h<2)
printf("02:20\n");
else if(h==2&&m<20)
printf("02:20\n");

else if(h<3)
printf("03:30\n");
else if(h==3&&m<30)
printf("03:30\n");

else if(h<4)
printf("04:40\n");
else if(h==4&&m<40)
printf("04:40\n");

else if(h<5)
printf("05:50\n");
else if(h==5&&m<50)
printf("05:50\n");

else if(h<10)
printf("10:01\n");
else if(h==10&&m<1)
printf("10:01\n");

else if(h<11)
printf("11:11\n");
else if(h==11&&m<11)
printf("11:11\n");

else if(h<12)
printf("12:21\n");
else if(h==12&&m<21)
printf("12:21\n");

else if(h<13)
printf("13:31\n");
else if(h==13&&m<31)
printf("13:31\n");

else if(h<14)
printf("14:41\n");
else if(h==14&&m<41)
printf("14:41\n");

else if(h<15)
printf("15:51\n");
else if(h==15&&m<51)
printf("15:51\n");

else if(h<20)
printf("20:02\n");
else if(h==20&&m<02)
printf("20:02\n");

else if(h<21)
printf("21:12\n");
else if(h==21&&m<12)
printf("21:12\n");

else if(h<22)
printf("22:22\n");
else if(h==22&&m<22)
printf("22:22\n");

else if(h<23)
printf("23:32\n");
else if(h==23&&m<32)
printf("23:32\n");

else
printf("00:00\n");
}
return 0;
}