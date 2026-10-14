#include<bits/stdc++.h>

using namespace std;

ifstream fin("input.txt");

ofstream fout("output.txt");

int main(){

	string a;

	fin>>a;

	int b;

	fin>>b;

	if((a=="front" && b==1)||(a=="back" && b==2))

		fout<<'L';

	else 

		fout<<'R';

}