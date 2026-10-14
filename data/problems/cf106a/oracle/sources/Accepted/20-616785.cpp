#include<iostream>

using namespace std;

int find(char a){
	if(a=='6')return 1;
	else if(a=='7')return 2;
	else if(a=='8')return 3;
	else if(a=='9')return 4;
	else if(a=='T')return 5;
	else if(a=='J')return 6;
	else if(a=='Q')return 7;
	else if(a=='K')return 8;
	else if(a=='A')return 9;
}

int main()
{
//	freopen("sam.txt","r",stdin);
	char trum,sut1,sut2,rank1,rank2,temp;
	cin>>trum;
	cin>>rank1>>sut1>>rank2>>sut2;
	if(trum!=sut2 && trum==sut1)cout<<"YES"<<endl;
	else if(trum==sut1 && trum==sut2 && find(rank1)>find(rank2))cout<<"YES"<<endl;
	else if(sut1==sut2 && find(rank1)>find(rank2))cout<<"YES"<<endl;
	else cout<<"NO"<<endl;
	return 0;
}