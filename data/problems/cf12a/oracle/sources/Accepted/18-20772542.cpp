#include <iostream>

#include <iomanip>

#include <algorithm>

#include <cmath>

#include <map>

#include <set>

#include <stack>

#include <vector>

#include <queue>



using namespace std;



int main()

{

    ios_base::sync_with_stdio(false);

    char a[3][3];

    for(int i=0;i<3;i++)

    {

        for(int j=0;j<3;j++)

        {

            cin>>a[i][j];

        }

    }

    for(int i=0;i<3;i++)

    {

        for(int j=0;j<3;j++)

        {

            if(a[i][j]!=a[2-i][2-j])

            {

                cout<<"NO";

                return 0;

            }

        }

    }

    cout<<"YES";

    return 0;

}