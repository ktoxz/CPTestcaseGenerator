#include <iostream>
#include <algorithm> 
#include <math.h>
#include <vector>
#include <set>
#include <string>
using namespace std;
int main()
{	
	char A[] = {'6', '7', '8', '9', 'T', 'J', 'Q', 'K' , 'A'};
	int i,val1,val2;
	char trump,rank1,rank2,suit1,suit2;
	cin >> trump;
	cin >> rank1 >> suit1 >> rank2 >> suit2;
	if((suit1==trump)&&(suit2!=trump))	
		cout << "YES" << endl;
	else if(suit1!=suit2)
		cout << "NO" << endl;
	else
	{
		for(i=0;i<9;i++)
		{
			if(rank1 == A[i])
				val1 = i;
			if(rank2 == A[i])
				val2 = i;
		}
		if(val1>val2)
			cout << "YES" << endl;
		else
			cout << "NO" << endl;
	}
	return 0;
}