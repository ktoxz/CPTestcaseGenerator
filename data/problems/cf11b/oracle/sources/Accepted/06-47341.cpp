#include <iostream>
using namespace std;
int main(){
	int n;
	int i,j,k,x;
	
	cin>>n;
	if(n<0)n = -n;
	k=0; j=1; x=0; 
	while((k-n)<0 || (k-n)%2!=0){
		k += j;
		j++;
		x++;
	}
	cout<<x<<endl;
	return 0;
}