#include <iostream>



using namespace std;

int main(){

    int k,l;

    cin>>k>>l;

    int ans=0;

    while(l%k==0)

        l/=k,ans++;

    if(l!=1)

        cout<<"NO";

    else

        cout<<"YES"<<endl<<ans-1;

}