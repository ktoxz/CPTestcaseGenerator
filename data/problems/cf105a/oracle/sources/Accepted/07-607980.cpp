#include <cstdio>
#include <string>
#include <map>
#include <algorithm>
using namespace std;

int main(){
    int n,m,e,k;
    double co;
    char name[100];
    scanf("%d%d%lf",&n,&m,&co);
    k=int(co*100+0.5);
    map<string,int> u;
    for(int i=0;i<n;i++){
        scanf("%s%d",name,&e);
        if(e*k>=10000) u[name]=e*k/100;
    }
    for(int i=0;i<m;i++){
        scanf("%s",name);
        u[name]*=1;
    }
    printf("%d\n",u.size());
    for(auto& x:u) printf("%s %d\n",x.first.c_str(),x.second);
}