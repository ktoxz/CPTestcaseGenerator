#include <iostream>
#include <vector>
#include <cstdio>
#include <stdlib.h>
#include <stdio.h>
#include <cctype>
#include <map>
#include <math.h>
#include <algorithm>
#define _getchar_nolock getchar 
#define _putchar_nolock putchar 
using namespace std;

int main()
{
	int n;
	cin >> n;
	string a, b;
	char c1, c2;
	cin >> a >> b;
	int cnt = 0;
	for(int i = 0; i < n / 2; i++)
	{
		c1 = b[i];
		c2 = b[n - i - 1];
		string temp2;
		temp2 += c1;
		temp2 += c2;
		string temp1;
		temp1 += a[i];
		temp1 += a[n-i-1];
		
		//cout << temp1 << ' ' << temp2 << ' ';
		if((temp1[0] == temp2[0] && temp1[1] == temp2[1]) || (temp1[1] == temp2[0] && temp2[1] == temp1[0]) || (temp1[0] == temp1[1] && temp2[0] == temp2[1]))
		{
			 cnt += 0;
			 continue;
		}
				if(temp2[0] == temp2[1] && temp1[0] != temp2[0] && temp1[0] != temp2[0] && temp1[1] != temp2[0]) 
				{
					cnt++;
					continue;
				}
		if(temp1[0] == temp2[0])
		{
			 temp1.erase(temp1.begin());
			 temp2.erase(temp2.begin());
		}
		else
		if(temp1[0] == temp2[1])
		{
			 temp1.erase(temp1.begin());
			 temp2.erase(temp2.begin() + 1);
		}
		
		if(temp1.size() > 1)
		{
			if(temp1[1] == temp2[0])
			{
				temp1.erase(temp1.begin() + 1);
			 	temp2.erase(temp2.begin());
			}
			else
			if(temp1[1] == temp2[1])
			{
				 temp1.erase(temp1.begin() + 1);
			 	temp2.erase(temp2.begin() + 1);
			}	
		}	
		cnt += temp1.size();
		//cout << cnt << '\n';	
	}
	if(n % 2 != 0)
	{
		if(a[n/2] != b[n/2]) cnt++;
	}
	cout << cnt;
}