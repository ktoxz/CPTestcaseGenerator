#include <iostream>
#include <string>

using namespace std;

int main()
{
	/* code */
	string s;
	cin >> s;
	int ans = 0;
	int arr[2];
	arr[0] = (s[0] - '0')%3;
	int bar = -1;

	for(int i = 0; i < s.length(); i++)
	{
		int k = (s[i] - '0')%3;
		if(k == 0)
		{
			ans++;
			bar = i;
		}
		else if(i - bar >= 2 && i > 0 && arr[0] + k == 3)
		{
			ans++;
			bar = i;
		}
		else if(i - bar >= 3 && i > 1 && (arr[0] + arr[1] + k)%3 == 0 )
		{
			ans++;
			bar = i;
		}


		if(i > 0)
		{
			arr[1] = arr[0];
			arr[0] = k;
		}
		//cout << bar << endl;
	}
	cout << ans;
	return 0;
}