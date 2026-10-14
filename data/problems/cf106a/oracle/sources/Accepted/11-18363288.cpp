#include<bits/stdc++.h>

using namespace std;

int main(){





	string s = "6789TJQKA",a,b;

	char x;

	cin >> x;

	cin >> a >> b;

	map<char, int>mp;

	for (int i = 0; i < s.size(); i++)

		mp[s[i]] = i;

	if (a[1] == b[1]){

		if (mp[a[0]]>mp[b[0]])

			puts("YES");

		else puts("NO");

	}

	else if (x == a[1])

		puts("YES");

	else puts("NO");

	



return 0;

}