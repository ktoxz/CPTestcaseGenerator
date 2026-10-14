#include<bits/stdc++.h>

using namespace std;

int main()

{

	char arr[3][3];

	for(int i=0;i<3;i++)for(int j=0;j<3;j++)cin>>arr[i][j];

	if(!(arr[1][0]==arr[1][2] && arr[0][1]==arr[2][1] && arr[0][0]==arr[2][2] && arr[0][2]==arr[2][0]))

		cout<<"NO\n";

	else

		cout<<"YES\n";

	return 0;

}



/*

00 01 02

10 11 12

20 21 22

*/