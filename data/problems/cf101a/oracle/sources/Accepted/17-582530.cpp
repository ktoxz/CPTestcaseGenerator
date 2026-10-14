#include <string>
#include <algorithm>
#include <set>
#include <vector>
#include <iostream>

using namespace std;

inline bool compare(const vector<int>& a, const vector<int>& b)
{
	return a.size() < b.size();
}

int main ()
{
	string s;
	int k;
	cin >> s >> k;
	k = min(k, (int)s.size());

	vector<int> chars[128];
	set<char> charset;
	
	for (int i = 0; i < s.size(); i++)
	{
		chars[s[i]].push_back(i);
		charset.insert(s[i]);
	}
	sort(chars + 'a', chars + 'z' + 1, compare);

	bool deleted[100001] = { false };
	int rem_count = charset.size();
	int cur_char = 'a';
	while (k)
	{
		while (chars[cur_char].empty())
			cur_char++;
		deleted[*(chars[cur_char].end()-1)] = true;
		k--;
		chars[cur_char].erase(chars[cur_char].end()-1);
		if (chars[cur_char].empty())
			rem_count--;
	}
	cout << rem_count << endl;
	for (int i = 0; i < s.size(); i++)
	{
		if (!deleted[i])
			cout << s[i];
	}
	cout << endl;
}