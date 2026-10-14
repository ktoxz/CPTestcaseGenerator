#include <string>
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
typedef pair<int, int> pair_t;
vector<pair_t> vp;
const string MARK[2][3] = {{"lios", "etr", "initis"}, {"liala", "etra", "inites"}};
int cnt[3];
void noSol()
{
	printf("NO\n");
	exit(0);
}

pair_t endWith(string str)
{
	int l2 = str.length();
	for(int i = 0; i < 2; i ++)
		for(int j = 0; j < 3; j ++)
		{
			int l = MARK[i][j].length();
			if(l2 >= l && str.substr(l2 - l, l) == MARK[i][j])
				return make_pair(i, j);
		}
	return make_pair(-1, -1);
}

int main()
{
	//freopen("t.in", "r", stdin);
	string str;
	while(cin >> str)
	{
		for(int i = 0; i < (int)str.length(); i ++)
			if(!('a' <= str[i] && str[i] <= 'z'))
				noSol();
		pair_t P = endWith(str);
		if(P.first == -1)
			noSol();
		vp.push_back(P);
	}
	if(vp.size() == 0)
		noSol();
	else if(vp.size() == 1)
	{
		printf("YES\n");
		return 0;
	}
	int gender = vp[0].first;
	for(int i = 0; i < (int)vp.size(); i ++)
		if(gender != vp[i].first)
			noSol();

	for(int i = 0; i < (int)vp.size(); i ++)
	{
		int st = i, en = i;
		while(en + 1 < (int)vp.size() && vp[en].second == vp[en + 1].second)
			en ++;
		int type = vp[en].second;
		if(cnt[type] != 0 || (type == 2 && cnt[1] == 0) ||(type == 0 && cnt[1] != 0))
			noSol();
		cnt[type] = en - st + 1;
		i = en;
	}
	if(cnt[1] != 1)
		noSol();
	printf("YES\n");
}