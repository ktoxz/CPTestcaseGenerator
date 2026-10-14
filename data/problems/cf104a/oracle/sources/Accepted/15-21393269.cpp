#include <iostream>



using namespace std;

int n;

int arr[12]={0,4,4,4,4,4,4,4,4,4,15,4};



int main()

{

    cin >> n;

    if (n>=10){

        cout << arr[n-10] << endl;

    }else{

        cout << arr[0] << endl;

    }

    return 0;

}