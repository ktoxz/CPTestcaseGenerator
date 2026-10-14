#include <bits/stdc++.h>

using namespace std;

string napis, s, a , b;
int n, licz, wyn, suma, odw[100];

int main()
{
        ios::sync_with_stdio(false);
    cin>>n;
    cin >> a;
    cin >> b;
    for (int i=0; i<n/2; i++)
    {
        int kan=0;
        if (b[i]==b[n-i-1])
        {
            if(a[i]==a[n-i-1])
            {
                kan=0;
            }
            else
            {
                kan=1;
            }
        }
        else if(b[i]!=b[n-i-1])
        {
            if (a[i]==b[i] && a[n-i-1]==b[n-i-1])
            {
                kan=0;
            }
            else if (a[i]==b[n-i-1] && a[n-i-1]==b[i])
            {
                kan=0;
            }
            else if(a[i]==b[i] || a[i]==b[n-i-1])
            {
                kan=1;
            }
            else if(a[n-i-1]==b[i] || a[n-i-1]==b[n-i-1])
            {
                kan=1;
            }
            else
            {
                kan=2;
            }
        }
        wyn+=kan;
        //cout << i << " " << kan << endl;
    }
    if ((n%2)==1)
    {
        if (a[n/2]!=b[n/2])
        {
            wyn++;
            //cout << n/2 << " " << 1 << endl;
        }
    }
    cout << wyn;
}