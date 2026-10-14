#include <bits/stdc++.h>



using namespace std;

multiset < int > ms;

int a[100009] , b[100009];

int main()

{

    memset(a , -1 , sizeof(a));

    string s , s1;

    cin >> s >> s1;

    if(s.size() > s1.size() || s.size() < s1.size())

    {

        cout << "WRONG_ANSWER" << endl;

        return 0;

    }

    bool b1 = 0;

    for(int i=0;i<s.size();i++)

    {

        if(!(s[i] == s1[i] && s[i] =='0'))

        {

            b1 = 1;

        }

    }

    if(!b1)

    {

        cout << "OK" << endl;

        return 0;

    }

    for(int i=0;i<s.size();i++)

    {

        if(s[i] != '0')

        ms.insert(s[i] - '0');

    }

    for(int i=0;i<s1.size();i++)

        b[i] = s1[i] - '0';

    int i=0;

    for(multiset < int > :: iterator it = ms.begin();it!=ms.end();it++,i++)

    {

        if(i == 1)

        {

            int h = i;

            for(int j=1;j<s.size() - ms.size() + h;j++){

                a[j] = 0;

                i++;

            }

        }

        a[i] = (*it);

    }

    for(int i=0;i<s1.size();i++)

    {

        if(a[i] != b[i]){

            cout << "WRONG_ANSWER" << endl;

            return 0;

        }

    }

    cout << "OK" << endl;

    return 0;

}