#include <iostream>
#include <fstream>

using namespace std;

int main()
{
	ifstream ifile("input.txt");
	if(ifile) {
	       freopen("input.txt","rt",stdin);
	}
	if(ifile) {
		freopen("output.txt","wt",stdout);
	}
	while( !cin.eof() ) {
		string s;
		int a;
		cin >> s;
		cin >> a;
		if( s.size() != 0 ) {
			if( s.compare("front") == 0 ) {
			       if( a == 1 ) {
					cout << "L";
			       } else {
				       cout << "R";
			       }
			} else {
				if( a == 1 ) {
					cout << "R";
			   	} else {
					cout << "L";
			       	}
			}
			cout << endl;
		}
	}
	return 0;
}