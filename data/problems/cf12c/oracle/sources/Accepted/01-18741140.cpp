#include <iostream>

#include<bits/stdc++.h>

using namespace std;

int arr[150],fr[150];

int main()

{

    int n,m;

    cin>>n>>m;

    for(int i = 0 ; i<n ; i++)

    {

       cin>>arr[i];

    }

    map<string,int>mp;

    for(int i = 0 ; i<m ; i++)

    {

        string s;

        cin>>s;

        mp[s]++;

    }

    int k = 0;

    for(map<string , int>::iterator it = mp.begin()  ; it!=mp.end() ; it++,k++)

    {

        fr[k] = it->second;

    }

    sort(arr,arr+n);

    sort(fr,fr+k);

    reverse(fr,fr+k);

    int ans1 = 0 , ans2 = 0;

    for(int i = 0 ; i<k ; i++) ans1+=arr[i]*fr[i];

    for(int i = 0 ; i<k ; i++) ans2+=arr[n-i-1]*fr[i];

    cout<<ans1<<" "<<ans2;

    return 0;

}