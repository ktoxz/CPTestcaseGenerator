#include<iostream>
#include<algorithm>

using namespace std;

int main()
{
    string s;int k;
    cin >> s >>k;
    int arr[27]={0};
    for(int i=0;i<s.length();i++)
    {
        arr[((int)s[i])-96]++;
    }
    while(k>0)
    {
        int min=999999999;
        int pos=0;
        for(int i=1;i<27;i++)
        {
            if(min>arr[i] && arr[i]!=0)
            {   
                min=arr[i];
                pos=i;
            }
        }
        
        if(min<=k)
        {
            arr[pos]=0;
            k=k-min;
        }
        else
            k=0;
    }
    int count=0;
    for(int i=1;i<27;i++)
        if(arr[i]!=0)
            count++;
    cout << count<<endl;
    string s1="";
    for(int i=0;i<s.length();i++)
    {
        if(arr[((int)s[i]-96)]!=0)
        {
            s1=s1+s[i];
        }
    }
    
        cout<<s1<<endl;
    return 0;
}