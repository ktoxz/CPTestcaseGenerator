#include <bits/stdc++.h>

using namespace std;

int main()

{

    //freopen("cin.txt","r",stdin);

    int n,i,j,k,x,y,t1,t2,flag,sum;

    flag=sum=0;

    cin>>n>>i>>j>>k>>x>>y;

    while(n--){

        cin>>t1>>t2;

        if(flag!=t1&&flag){

            flag=t1-flag;

            if(flag>=x){

                sum+=x*i;

                flag-=x;

            }

            else{

                sum+=flag*i;

                flag=0;

            }

            if(flag>=y){

                sum+=y*j;

                flag-=y;

            }

            else{

                sum+=flag*j;

                flag=0;

            }

            if(flag){

                sum+=flag*k;

            }

        }

        sum+=(t2-t1)*i;

        flag=t2;

    }

    cout<<sum<<endl;

    return 0;

}