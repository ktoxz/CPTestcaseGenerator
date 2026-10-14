#include <iostream>
#include <sstream>
#include <string>
using namespace std;

string str;

int toInt()
{
	int ret = 0;
	for (int i=0; i<str.size(); i++)
		ret += str[i]-'0';

	return ret;
}

void toStr(int n)
{
	stringstream ss;
	ss << n;
	ss >> str;
}

int main()
{
	cin >> str;

	int c=0;
	while (str.size() > 1)
	{
		int num = toInt();
		toStr(num);
		c++;
	}

	cout << c << endl;
}