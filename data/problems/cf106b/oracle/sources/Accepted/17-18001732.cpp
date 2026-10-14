#include "stdio.h"

#include "vector"

#include "algorithm"

using namespace std;

class state{

    public: int w,x,y,z,n;

};

bool compare(state x,state y){

    return x.w<y.w;

}

int main(){

    int n;

    scanf("%d",&n);

    vector<state> d(n);

    for(int i=0;i<n;i++) scanf("%d %d %d %d",&d[i].x,&d[i].y,&d[i].z,&d[i].w),d[i].n=i+1;

    sort(d.begin(),d.end(),compare);

    for(int i=0;i<n;i++){

        bool check=false;

        for(int j=0;j<n;j++){

            if(d[j].x>d[i].x&&d[j].y>d[i].y&&d[j].z>d[i].z){

                check=true;

                break;

            }

        }

        if(!check){

            printf("%d",d[i].n);

            break;

        }

    }

}