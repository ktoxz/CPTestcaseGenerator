#include<iostream>

using namespace std;



int main()

{

    int n,d,i,cnt=0,x;

    cin>>n>>d;

    int arr[n];

    cin>>arr[0];

    for(i=1;i<n;i++)

    {

        cin>>arr[i];

        if(arr[i]<=arr[i-1])

        {

            x = (arr[i-1]-arr[i] + d)/d; 

            arr[i] +=d*x;

            cnt = cnt + x;  

        }

    }

    cout<<cnt<<endl;

    return 0;

}