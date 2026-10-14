#include<algorithm>
#include<cstring>
#include<cstdio>
using namespace std;
int n,dec[4]={0,21,14,7},num[4]={0,3,2,1},cnt;
int main(){
    scanf("%d",&n);
    int c=n%4;
    if(n<dec[c]){
        printf("-1\n");
        return 0;
    }
    n-=dec[c];
    cnt=num[c];
    while(n>=28){
        n-=28;
        cnt+=4;
    }
    for(int i=1;i<=n/4;++i)
        printf("4");
    for(int i=1;i<=cnt;++i)
        printf("7");
    return 0;
}