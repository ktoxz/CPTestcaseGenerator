#include <iostream>

#include <stdio.h>

#include <algorithm>

#include <math.h>

#include <sstream>

#include <fstream>

#include <vector>

#include <cstring>

#include <string>

#include <queue>

#include <map>

#include <set>

#include <bitset>

#include <stdlib.h>

#include <ctime>

using namespace std;

#define forr(n) for(ll i=0;i<n;i++)

#define forrr(n) for(unsigned long long i=1;i<n;i++)

#define forb(n) for(long long i=n-1;i>=0;i--)

#define PI (double)3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862

#define MOD 1000000007

typedef long long int ll;

typedef long double ld;

typedef vector< ll > llvector;

typedef vector<string> svector;

typedef vector< pair<ll,ll> > pairsvector; //pairs.push_back(make_pair(temp1,temp2)); scanf("%ld %ld\n", &data[p].first, &data[p].second);

typedef vector< pair< pair<ll,ll> , bool > > pairsboolvector;

typedef set<int> yset;

typedef map<ll,char> ymap;

typedef priority_queue<ll> ypq;

typedef pair<ll,ll> ypair;

typedef bitset<32>  ybitset;

void                      printvictor(vector<ll> v){forr(v.size())cout<<v[i]<<" ";cout<<endl;}

void                      printPQ(priority_queue<ll> pq){while (!pq.empty()){cout<<pq.top()<<" ";pq.pop();}std::cout << '\n';}

template <class T> string toStr(const T &x){ stringstream s; s << x; return s.str(); }

template <class T> ll     toInt(const T &x){ stringstream s; s << x; ll r; s >> r; return r; }

bool                      isprime(ll n) {if(n == 2)  return true;if(n < 2 || n%2 == 0)   return false;for(ll i=3; i*i <= n; i+=2){if(n%i == 0)return false;}return true;}

vector<ll>                generate_divisors(ll n){vector<ll> v;ll i;for(i = 1 ; i <=  n  ;++i)if(n%i == 0)v.push_back(i);return v;}

ll 		BinaryToDec(string binary){ll arr[binary.length()];ll sum=0;forr(binary.length())arr[i] = pow(2,i);reverse(binary.begin(),binary.end());forr(binary.length())if(toInt(binary[i]) == 1)sum+=arr[i];return sum;}

string  DecToBinary(ll decimal){string binary = "";while(true){if(decimal %2 ==0)binary += '0';else binary += '1';if(decimal==1)break;decimal /= 2;}reverse(binary.begin(),binary.end());return binary;}

ll     gcd(ll a, ll b) {return b == 0 ? a : gcd(b, a%b);}

//--------------------------------------------------------------------YASSER ALAA ELDIN--------------------------------------------------------------------------

int main()

{

    ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);

    #ifndef ONLINE_JUDGE

    freopen("in.txt","r", stdin);

    freopen("out.txt","w", stdout);

    #endif

 	int n,m;

 	cin>>n>>m;

 	std::vector<int> tags(n);

 	std::vector<string> vec(m);

 	std::vector<int> fruits;

 	forr(n)

 	cin>>tags[i];

 	forr(m)

 	cin>>vec[i];



 	sort(vec.begin(),vec.end());

 	int sum=1;

 	forrr(vec.size())

 	{

 		if(vec[i]==vec[i-1])

 			sum++;

 		else

 			fruits.push_back(sum),sum=1;

 	}

 		fruits.push_back(sum);



 		int maxone=0,minone=0;

 		sort(tags.begin(),tags.end());

 		sort(fruits.rbegin(),fruits.rend());

 		forr(fruits.size())

 		minone += fruits[i]*tags[i];



 		sort(tags.rbegin(),tags.rend());

 		forr(fruits.size())

 		maxone += fruits[i]*tags[i];

 		



 		cout<<minone<<" "<<maxone<<endl;

	return 0;

}