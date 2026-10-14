#include<iostream>

using namespace std;



int main()

{

    char a[3][3];

    int i,j,flag=0,n=3;

    for(i=0;i<n;i++){for(j=0;j<n;j++)   cin>>a[i][j];}

    if(a[0][0]==a[2][2]&&a[0][1]==a[2][1]&&a[0][2]==a[2][0]&&a[1][0]==a[1][2])  cout<<"YES";

    else    cout<<"NO";

    /*for(i=0;i<n;i++)

    {

        int k=n-i-1;

        for(j=0;j<n;j++)

        {   

            if(a[i][j]!=a[k][3-j])   {flag=1;break;}

        }

    }

    if(flag==0) cout<<"YES";

    else    cout<<"NO";*/

    return 0;

}