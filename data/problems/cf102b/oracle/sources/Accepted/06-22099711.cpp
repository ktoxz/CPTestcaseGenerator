#include <iostream>

#include<string>

#include<algorithm>

using namespace std;

int main()

{

    string s;

    int num=1;

    long long sum=0;

    int x[20]={0};

    cin>>s;

    if(s.size()==1)

    {

        cout<<0;

        return 0;

    }

    for(int i=0;i<s.size();i++)

    {

        x[s[i]-'0']++;

    }

    for(int i=0;i<10;i++)

    {

        sum+=i*x[i];

    }

    if(sum<10)

    {

        cout<<1;

        return 0;

    }

    do

    {

        num++;

        int temp=sum;

        sum=0;

        while(temp)

        {

            sum+=temp%10;

            temp=temp/10;

        }

    }while(sum>=10);

    cout<<num;

}