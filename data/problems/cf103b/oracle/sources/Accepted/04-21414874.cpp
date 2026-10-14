#include <bits/stdc++.h> 

using namespace std;



vector <int> P;

vector <int> S;



void create (int v)

{

	P.push_back(v);

	S.push_back(1);

}



int find (int x) {return x == P[x] ? x : (P[x] = find(P[x]));}



bool unionS (int x, int y)

{

	x = find(x);

	y = find(y);

	if (x == y) return 0;

	if (S[x] > S[y])

	{

		S[x] += S[y];

		P[y] = x;

	}

	else

	{

		S[y] += S[x];

		P[x] = y;

	}

	return 1;

}



int main()

{

	int n,m,u,v;

	scanf("%d%d",&n,&m);

	bool anw = 0;

	for (int i = 0; i <= n; i++) create(i);

	for (int i = 0; i < m; i++)

	{

		scanf("%d%d",&u,&v);

		bool f = unionS(u,v);

		if (!f && anw)

		{

			printf("NO\n");

			return 0;

		}

		else if (!f) anw = 1;

	}

	set <int> d;

	for (int i = 1; i <= n; i++) d.insert(find(i));

	printf(anw && d.size() == 1 ? "FHTAGN!\n" : "NO\n");

}