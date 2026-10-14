// topcoder.cpp : �R���\�[�� �A�v���P�[�V�����̃G���g�� �|�C���g���`���܂��B
//

#include <stdio.h>
#include <string.h>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <climits>
#include <cfloat>
#include <map>
#include <utility>
#include <set>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <algorithm>
#include <functional>
#include <sstream>
#include <complex>
#include <stack>
#include <queue>
#include <numeric>
#include <assert.h>
#include <iomanip>
#include <bitset>
#include <time.h>
#include <math.h>

using namespace std;
typedef long long ll;

static const double EPS = 1e-9;
int ROUND(double x) { return (int)(x+0.5); }
bool ISINT(double x) { return fabs(ROUND(x)-x)<=EPS; }
bool ISEQUAL(double x,double y) { return fabs(x-y)<=EPS*max(1.0,max(fabs(x),fabs(y))); }
double SQSUM(double x,double y) { return x*x+y*y; }	
#define PI	(2.0*acos(0.0))
template<class T> bool INRANGE(T x,T a,T b) { return a<=x&&x<=b; }
#define NG (-1)
#define SZ(a) ((int)a.size()) 

#define BIG (100000)


vector <int> a[105];
int visited[105];
int passed[105];
int num_cycles;
int N,M;

#if 1

void dfs(int last_x,int x)
{
	if(visited[x])
	{
// 		printf("CYCLE!\n");
// 		printf("last_x=%d x=%d VISITED ",last_x,x);
// 		for(int i=0;i<N;i++)
// 		{
// 			printf("%d ",visited[i]);
// 		}
// 		printf("\n");

		num_cycles++;
		return;
	}

	if(num_cycles>=3)
	{
		return;
	}

	visited[x]=1;
// 	printf("VISITED ");
// 	for(int i=0;i<N;i++)
// 	{
// 		printf("%d ",visited[i]);
// 	}
// 	printf("\n");
// 
// 	printf("PASSED ");
// 	for(int i=0;i<N;i++)
// 	{
// 		printf("%d ",passed[i]);
// 	}
// 	printf("\n");

	passed[x]=1;
	for(int i=0;i<SZ(a[x]);i++)
	{
		if(last_x!=a[x][i])
		{
			dfs(x,a[x][i]);
		}
	}

	visited[x]=0;
}


int main()
{
	// ���I ��o�O�ɏ����I
//	freopen("input.txt","r",stdin);

	scanf("%d %d",&N,&M);
	if(M==0)
	{
		printf("NO\n");
		return 0;
	}

	for(int i=0;i<N;i++)
	{
		a[i].clear();
	}

	for(int k=0;k<M;k++)
	{
		int s,e;
		scanf("%d %d",&s,&e);
		s--;
		e--;
		a[s].push_back(e);
		a[e].push_back(s);
	}

	memset(visited,0,sizeof(visited));
	memset(passed,0,sizeof(passed));
	num_cycles = 0;

	dfs(-1,0);

	bool ok = true;
	for(int i=0;i<N;i++)
	{
		if(passed[i]==0)
		{
			ok = false;
		}
	}

	if(num_cycles==2 && ok)
	{
		printf("FHTAGN!\n");
	}
	else
	{
		printf("NO\n");
	}


/*
	for(int i=0;i<N;i++)
	{
		for(int j=0;j<N;j++)
		{
			printf("%6d ",a[i][j]);
		}
		printf("\n");
	}
*/

}

#elif 1
	int main()
{
	// ���I ��o�O�ɏ����I
	//	freopen("input.txt","r",stdin);

	ll N;
	ll ret = 0LL;

	cin >> N;
	for(int i=0;i<N;i++)
	{
		ll a;
		cin >> a; 
		ret += (a-1LL)*(i+1LL)+1LL;
	}
	cout << ret << endl;

}

#elif 1
	int main()
{
	// ���I ��o�O�ɏ����I
	//	freopen("input.txt","r",stdin);

	int K,N;
	scanf("%d %d",&N,&K);

	vector < vector <int> > yama;

	vector <int> ans(N,0);

	for(int y=0;y<K;y++)
	{
		vector <int> vi;
		for(int n=0;n<N/2;n++)
		{
			int tmp;
			scanf("%d ",&tmp);
			vi.push_back(tmp);
		}
		yama.push_back(vi);
	}

	int count = 0;

	for(int i=0;i<4*N/8;i++)
	{
		ans[i]=1;
	}

	int a = rand()%N;
	int b = 0;
	while(1)
	{
		while(ans[a]==ans[b])
		{
			a = rand()%N;
		}
		swap(ans[a],ans[b]);

		bool ok = true;
		for(int y=0;y<K;y++)
		{
			int sum = 0;
			for(int n=0;n<SZ(yama[y]);n++)
			{
				sum += ans[yama[y][n]-1];
			}

			if(!INRANGE(sum*8,N,3*N))
			{
				ok = false;
				b = yama[y][rand()%SZ(yama[y])]-1;
				break;
			}
		}

		if(ok)
		{
			for(int i=0;i<N;i++)
			{
				printf("%d",ans[i]);
			}
			printf("\n");
			exit(0);
		}
	}
}

#elif 0

	void yama_sort(	vector < vector <int> >& yama, int H, int W, int summit_x)
{
	vector < pair < int, vector <int> > > yama2;
	for(int y=0;y<H;y++)
	{
		yama2.push_back(make_pair(yama[y][summit_x],yama[y]));
	}

	sort(yama2.begin(),yama2.end());

	for(int y=0;y<SZ(yama2);y++)
	{
		for(int x=0;x<SZ(yama2[y].second);x++)
		{
			printf("%d ",yama2[y].second[x]);
		}
		printf("\n");
	}

	for(int y=0;y<H;y++)
	{
		yama[y] = yama2[y].second;
	}
}

void yama_tenchi(vector < vector <int> >& yama, int H, int W)
{
	vector < vector <int> > yama2(W, vector <int> (H,0));

	for(int y=0;y<H;y++)
	{
		for(int x=0;x<W;x++)
		{
			yama2[x][y]=yama[y][x];
		}
	}
	yama=yama2;
}

int main()
{
	// ���I ��o�O�ɏ����I
	freopen("input.txt","r",stdin);

	int H,W;
	scanf("%d %d",&H,&W);

	vector < vector <int> > yama;

	int summit_y = -1;
	int summit_x = -1;
	int summit_h = -1;

	for(int y=0;y<H;y++)
	{
		vector <int> vi;
		for(int x=0;x<W;x++)
		{
			int tmp;
			scanf("%d ",&tmp);
			vi.push_back(tmp);
			if(tmp>summit_h)
			{
				summit_h = tmp;
				summit_y = y;
				summit_x = x;
			}
		}
		yama.push_back(vi);
	}

	// 	for(int y=0;y<SZ(yama);y++)
	// 	{
	// 		for(int x=0;x<SZ(yama[y]);x++)
	// 		{
	// 			printf("%d ",yama[y][x]);
	// 		}
	// 		printf("\n");
	// 	}
	// 	printf("\n");

	yama_sort(yama, SZ(yama), SZ(yama[0]), summit_x);
	yama_tenchi(yama, SZ(yama), SZ(yama[0]));
	yama_sort(yama, SZ(yama), SZ(yama[0]), SZ(yama[0])-1);

	bool ok = true;
	for(int y=0;y<SZ(yama);y++)
	{
		for(int x=0;x<SZ(yama[0]);x++)
		{
			if(y<SZ(yama)-1 && yama[y][x]>yama[y+1][x]) ok = false;
			if(x<SZ(yama[0])-1 && yama[y][x]>yama[y][x+1]) ok = false;
		}
	}

	if(ok)
	{
		printf("YES\n");
	}
	else
	{
		printf("NO\n");
	}


}


#elif 1


#define MAX_L		(2000000)
#define MAX_SQRT_B	(2000000)

	bool is_prime[MAX_L];
ll   factor[MAX_L];
bool is_prime_small[MAX_SQRT_B];

void segment_sieve(ll a,ll b)
{
	for(int i=0;(ll)i*i<b;i++)
	{
		is_prime_small[i]=true;
	}
	for(int i=0;i<b-a;i++)
	{
		is_prime[i]=true;
		factor[i]=a+i;
	}
	for(int i=2;(ll)i*i<b;i++)
	{
		if(is_prime_small[i])
		{
			for(int j=2*i;(ll)j*j<b;j+=i)
			{
				//				printf("%d false1\n",j);
				is_prime_small[j]=false;
			}
			for(ll j=max(2LL,(a+i-1)/i)*i;j<b;j+=i)
			{
				//				printf("%lld %d false2\n",j,i);
				if(is_prime[j-a]==true)
				{
					is_prime[j-a]=false;
					factor[j-a]=i;
				}
			}
		}
	}

}

void make_primes(int num, vector<int>& primes)
{
	primes.clear();
	primes.reserve(num);
	vector<int> no_prime;
	no_prime.resize(num+1);

	for(int i=2;i<=num;i++)
	{
		if(!no_prime[i])
		{
			primes.push_back(i);
			for(int j=i+i;j<=num;j+=i)
			{
				no_prime[j] = 1;
			}
		}
	}
}



vector<int> primes;
bool make_prime_factors(ll num, int k)
{
	ll base = num;
	ll j=primes[k];
	int e=0;
	int last_e=BIG;
	while(j*j<=base)
	{
		if(base%j==0)
		{
			base /= j;
			e++;
			if(e>last_e)
			{
				return false;
			}
		}
		else
		{
			k++;
			j=primes[k];
			if(e!=0)
			{
				last_e = e;
			}
			e=0;
		}
	}

	if(j==base)
	{
		e++;
		if(e>last_e)
		{
			return false;
		}
	}

	return true;
}

int main()
{
	// ���I ��o�O�ɏ����I
	//	freopen("input.txt","r",stdin);

	ll A,B;
	cin >> A >> B;

	ll a = A-B;
	ll b = A+B+1;

	primes.clear();
	make_primes(MAX_L, primes);

	map<ll, int> sosu_id;
	for(int i=0;i<SZ(primes);i++)
	{
		sosu_id[primes[i]]=i;
	}

	segment_sieve(a,b);

	int ret = 0;
	for(int i=0;i<b-a;i++)
	{
		if(is_prime[i])
		{
			//			printf("prime %d\n",a+i);
			ret++;
		}
		else if (make_prime_factors(a+i,sosu_id[factor[i]]))
		{
			//			printf("factors %d\n",a+i);
			ret++;
		}
	}
	printf("%d\n",ret);
}







#elif 1

	int main()
{
	set <string> st;
	char next_head = 'a';
	while(1)
	{

		string myword;

		while(1)
		{
			myword += string(1,next_head);
			for(int i=1;i<9;i++)
			{
				myword += string(1,'a'+(char)(rand()%26));
			}
			myword += 'a';
			if(st.count(myword)==0)
			{
				break;
			}
		}
		printf("?%s\n",myword.c_str()); fflush(stdout);
		st.insert(myword);

		char ai[1000];
		scanf("%s", ai);
		string aiword(ai);
		if(st.count(aiword) || aiword[0]!=myword[SZ(myword)-1])
		{
			printf("!OUT\n"); fflush(stdout);
			break;
		}
		next_head = aiword[SZ(aiword)-1];
		st.insert(aiword);
	}
}



#elif 0

	int main()
{
	// ���I ��o�O�ɏ����I
	//	freopen("input.txt","r",stdin);

	int H,W;
	scanf("%d %d ",&H,&W);

	vector <string> field;
	for(int i=0;i<H;i++)
	{
		char str[1000];
		scanf("%s",str);
		field.push_back(string(str));
	}

	vector < vector <int> > dist(H, vector <int> (W, BIG));


	dist[0][0]=0;
	for(int y=0;y<H;y++)
	{
		for(int x=0;x<W;x++)
		{
			for(int i=1;i<=H+W-2;i++)
			{
				if(y+x==i)
				{
					if(y==0)
					{
						dist[y][x]=field[y][x]-'0'+dist[y][x-1];
					}
					else if(x==0)
					{
						dist[y][x]=field[y][x]-'0'+dist[y-1][x];
					}
					else
					{
						dist[y][x]=field[y][x]-'0'+min(dist[y-1][x],dist[y][x-1]);
					}
				}
			}
		}
	}

	printf("%d\n",dist[H-1][W-1]);
}


#else

	int main()
{
	// ���I ��o�O�ɏ����I
	//	freopen("input.txt","r",stdin);

	char str[1000];
	scanf("%s",str);
	string s(str);
	int num[256]={};
	for(int i=0;i<SZ(s);i++)
	{
		num[s[i]]++;
	}
	int ret = min(num['K'],min(num['U'],min(num['P'],num['C'])));
	printf("%d\n",ret);
}
#endif