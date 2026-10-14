#include <iostream>



using namespace std;



bool marked[100+10];



int main()

{

    int number,help,min1=10000;

    cin>>number;

    int arr[number][4];

    for (int i=0;i<number;i++)

    {

        for (int j=0;j<4;j++)

        {

            cin>>arr[i][j];

        }

    }

    for (int i=0;i<number;i++)

    {

        int fcounter=0;

        for (int j=0;j<number;j++)

        {

            int counter=0;

            for (int k=0;k<3;k++)

            {

                if (arr[j][k]>arr[i][k])

                {

                    counter++;

                }

            }

            if (counter==3)

            {

                marked[i]=true;

            }

        }

    }

    for (int i=0;i<number;i++)

    {

        if (!marked[i] && min1>arr[i][3])

        {

            min1=arr[i][3];

            help=i;

        }

    }

    cout<<help+1;

    return 0;

}