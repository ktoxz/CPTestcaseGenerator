#include <stdio.h>
#include <iostream>
#include <cstdlib>
#include <sstream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
	int a, n;
	string s;

	ifstream fin ("input.txt");		//input file
	ofstream fout("output.txt");		//output file 

	fin >> s;
	fin >> a;

	fin.close();
	if(s == "front" && a == 1){
		fout<<"L\n";
	}
	else if(s == "front" && a == 2){
		fout<<"R\n";
	}
	else if(s == "back" && a == 1){
		fout<<"R\n";
	}
	else if(s == "back" && a == 2){
		fout<<"L\n";
	}
	fout.close();
	return 0;
}