#include<bits/stdc++.h>

using namespace std;

int main(){

	char tramp;

	cin>>tramp;

	char rank1,rank2,suit1,suit2;

	cin>>rank1>>suit1>>rank2>>suit2;

	if(tramp==suit1 && tramp!=suit2){

		cout<<"YES";

		return 0;

	}

	if(suit2!=suit1){

		cout<<"NO";

		return 0;

	}

	int a1,a2;

	if(rank1=='A')

		rank1='Z';

	if(rank1=='T')

		rank1='A';

	if(rank1=='J')

		rank1='B';

	if(rank1=='Q')

		rank1='C';

	if(rank2=='A')

		rank2='Z';

	if(rank2=='T')

		rank2='A';

	if(rank2=='J')

		rank2='B';

	if(rank2=='Q')

		rank2='C';

	if(rank1>rank2)

		cout<<"YES";

	else

		cout<<"NO";

}