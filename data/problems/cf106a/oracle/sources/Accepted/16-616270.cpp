#include <iostream>
#include <string>

using namespace std;

string order = "6789TJQKA";

int id( char c ){
	return order.find( c );
}

int main(){
	char trump ; 
	string A , B ;
	cin >> trump;
	cin >> A >> B;
	bool win = false;
	if( A[ 1 ] == B[ 1 ] ){ win = id( A[ 0 ] ) > id( B[0] ) ; }
	else{
		if( A[ 1 ] == trump ){ win = true; }
	}
	if( win ) 
		cout << "YES" << endl;
	else	
		cout << "NO" << endl;
	return 0;
}