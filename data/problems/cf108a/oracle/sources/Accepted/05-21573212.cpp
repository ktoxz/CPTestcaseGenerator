#include <iostream>



using namespace std;



int main()

{

    int num1,num2;

    char ch;

    cin>>num1>>ch>>num2;

    while (1)

    {

        num2++;

        if (num2==60)

        {

            num1++;

            num2=0;

        }

        if (num1==24)

        {

            num1=0;

        }

        if (num1%10==num2/10 && num2%10==num1/10)

        {

            if (num1<10)

            {

                cout<<0;

            }

            cout<<num1<<ch;

            if (num2<10)

            {

                cout<<0;

            }

            cout<<num2;

            return 0;

        }

    }

    return 0;

}