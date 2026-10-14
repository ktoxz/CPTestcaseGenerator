#define READ_NUM_TEST_CASES  false
#define USE_FAST_IO          false

////////////////////////////////////////////////////////////////////////////////
// AMALGAMATE: "include/template.hpp" BEGINS HERE
//
	
	
	#include <bits/stdc++.h>
	using namespace std;
	
	
	#if USE_FAST_IO
		
		////////////////////////////////////////////////////////////////////////////////
		// AMALGAMATE: "include/fast-io.hpp" BEGINS HERE
		//
			
			
			//#define FREAD  fread
			//#define FWRITE fwrite
			
			#define FREAD  fread_unlocked
			#define FWRITE fwrite_unlocked
			
			
			
			
			
			
			struct Buffer {
				FILE* const stream;
				const int buffer_size;
			
				uint8_t* const buff;
				int pos = 0;
			
				Buffer(FILE* a_stream, int a_buffer_size) :
						stream( a_stream ),
						buffer_size( a_buffer_size ),
						buff( new uint8_t[ buffer_size ] ) {
					setvbuf(stream, NULL, _IONBF, 0);
				}
			
				~Buffer() {
					delete[] buff;
				}
			};
			
			
			
			
			
			
			
			
			
			
			class In_Buffer : private Buffer {
			public:
				In_Buffer(FILE* a_stream, int a_buffer_size) : Buffer(a_stream, a_buffer_size) {
					FREAD(buff, 1, buffer_size, stream);
				}
			
			public:
				void prepare(int num_chars) {
					int remaining = buffer_size - pos;
					if(remaining >= num_chars) return;
			
					memcpy(buff, buff+pos, remaining);
			
					FREAD(buff+remaining, 1, pos, stream);
					pos = 0;
				}
			
			public:
				char get_unchecked() {
					return buff[ pos++ ];
				}
			};
			
			
			template<class INT>
			INT read_unsigned(In_Buffer& buff) {
				buff.prepare(25);
			
				char c = buff.get_unchecked();
				while(c < '-') c = buff.get_unchecked();
			
				INT r = 0;
			
				for(;;) {
					if(c < '0') return r;
					c -= '0';
					r = r*10 + c;
					c = buff.get_unchecked();
				}
			}
			
			
			template<class INT>
			INT read_signed(In_Buffer& buff) {
				buff.prepare(25);
			
				char c = buff.get_unchecked();
				while(c < '-') c = buff.get_unchecked();
			
				bool minus = false;
				if(c=='-') {
					c = buff.get_unchecked();
					minus = true;
				}
			
				INT r = 0;
			
				for(;;)
				{
					if(c < '0') return minus ? -r : r;
					c -= '0';
					r = r*10 + c;
					c = buff.get_unchecked();
				}
			}
			
			
			
			
			In_Buffer& operator>>( In_Buffer& buff, char& c) {
				buff.prepare(1);
				c = buff.get_unchecked();
				return buff;
			}
			
			
			
			In_Buffer& operator>>( In_Buffer& buff, uint16_t& r) { r = read_unsigned<uint16_t>(buff); return buff; }
			In_Buffer& operator>>( In_Buffer& buff, uint32_t& r) { r = read_unsigned<uint32_t>(buff); return buff; }
			In_Buffer& operator>>( In_Buffer& buff, uint64_t& r) { r = read_unsigned<uint64_t>(buff); return buff; }
			In_Buffer& operator>>( In_Buffer& buff, unsigned long long& r) { r = read_unsigned<unsigned long long>(buff); return buff; }
			
			In_Buffer& operator>>( In_Buffer& buff, int16_t& r) { r = read_signed<int16_t>(buff); return buff; }
			In_Buffer& operator>>( In_Buffer& buff, int32_t& r) { r = read_signed<int32_t>(buff); return buff; }
			In_Buffer& operator>>( In_Buffer& buff, int64_t& r) { r = read_signed<int64_t>(buff); return buff; }
			In_Buffer& operator>>( In_Buffer& buff, long long& r) { r = read_signed<long long>(buff); return buff; }
			
			In_Buffer& operator>>( In_Buffer& buff, string& r) {
				r.clear();
			
				char c = buff.get_unchecked();
				while(c <= ' ') c = buff.get_unchecked();
			
				do {
					r.push_back( c );
					c = buff.get_unchecked();
				} while(c > ' ');
			
				return buff;
			}
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			class Out_Buffer : private Buffer {
			public:
				Out_Buffer(FILE* a_stream, int a_buffer_size) : Buffer(a_stream, a_buffer_size) {}
			
				~Out_Buffer() {
					flush();
				}
			
			public:
				void prepare(int num_chars) {
					if(buffer_size - pos >= num_chars) return;
					flush();
				}
			
				void flush() {
					FWRITE(buff, 1, pos, stream);
					pos = 0;
				}
			
			public:
				void put_unchecked(const char& c) {
					buff[ pos++ ] = c;
				}
			
				void put_unchecked(const char* str, int len) {
					memcpy(buff+pos, str, len);
					pos += len;
				}
			};
			
			
			
			
			
			
			template<class INT>
			void write_signed(Out_Buffer& buff, const INT& i) {
				buff.prepare(25);
			
				if(i == 0) {
					buff.put_unchecked('0');
					return;
				}
			
				auto ci = i;
			
				if(ci < 0) {
					buff.put_unchecked('-');
					ci = -ci;
				}
			
				const int sz = 25;
				char temp[sz];
				int pos = sz;
			
				while(ci) {
					temp[ --pos ] = '0' + ci%10;
					ci/=10;
				}
			
				buff.put_unchecked(temp+pos, sz-pos);
			}
			
			
			
			template<class INT>
			void write_unsigned(Out_Buffer& buff, const INT& i) {
				buff.prepare(25);
			
				if(i==0) {
					buff.put_unchecked('0');
					return;
				}
			
				const int sz = 25;
				char temp[sz];
				int pos = sz;
			
				auto ci = i;
			
				while(ci) {
					temp[ --pos ] = '0' + ci%10;
					ci/=10;
				}
			
				buff.put_unchecked(temp+pos, sz-pos);
			}
			
			
			
			Out_Buffer& operator<<( Out_Buffer& buff, const char& c) {
				buff.prepare(1);
				buff.put_unchecked( c );
				return buff;
			}
			
			Out_Buffer& operator<<( Out_Buffer& buff, const uint16_t& r) { write_unsigned<uint16_t>(buff, r); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const uint32_t& r) { write_unsigned<uint32_t>(buff, r); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const uint64_t& r) { write_unsigned<uint64_t>(buff, r); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const ull& r) { write_unsigned<ull>(buff, r); return buff; }
			
			Out_Buffer& operator<<( Out_Buffer& buff, const int16_t& r) { write_signed<int16_t>(buff, r); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const int32_t& r) { write_signed<int32_t>(buff, r); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const int64_t& r) { write_signed<int64_t>(buff, r); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const ll& r) { write_signed<ll>(buff, r); return buff; }
			
			Out_Buffer& operator<<( Out_Buffer& buff, const char* cstr) { auto len = strlen(cstr); buff.prepare(len); buff.put_unchecked(cstr, len); return buff; }
			Out_Buffer& operator<<( Out_Buffer& buff, const string& str) { buff.prepare( str.size() ); buff.put_unchecked(str.data(), str.size()); return buff; }
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			#define BUFF_SIZE 32768
			In_Buffer  fast_cin(  stdin,  BUFF_SIZE );
			Out_Buffer fast_cout( stdout, BUFF_SIZE );
			//Out_Buffer fast_cerr( stderr, BUFF_SIZE );
			
			char fast_endl = '\n';
			
		
		//
		// AMALGAMATE: "include/fast-io.hpp" ENDS HERE
		////////////////////////////////////////////////////////////////////////////////
		
		#define cin fast_cin
		#define cout fast_cout
		#define cerr fast_cerr
		#define endl fast_endl
	#else
		
		////////////////////////////////////////////////////////////////////////////////
		// AMALGAMATE: "include/slow-io.hpp" BEGINS HERE
		//
			
			struct Slow_IO_Singleton {
				Slow_IO_Singleton() {
					ios_base::sync_with_stdio( false );
			
					std::cin.tie( nullptr );
					std::cout.tie( nullptr );
			
					setlocale(LC_ALL,"C");
			
					const int buffer_size = 32768;
			
					static char stdin_buffer[ buffer_size ];
					static char stdout_buffer[ buffer_size ];
			
					cin.rdbuf()->pubsetbuf( stdin_buffer, buffer_size );
					cout.rdbuf()->pubsetbuf( stdout_buffer, buffer_size );
				}
			
				~Slow_IO_Singleton() {
			
				}
			};
			
			
			Slow_IO_Singleton slow_io_singleton;
			
		
		//
		// AMALGAMATE: "include/slow-io.hpp" ENDS HERE
		////////////////////////////////////////////////////////////////////////////////
		
		#define endl '\n'
	#endif
	
	
	
	////////////////////////////////////////////////////////////////////////////////
	// AMALGAMATE: "include/debug.hpp" BEGINS HERE
	//
		
		
		#define ASS(x) assert(x)
	
	//
	// AMALGAMATE: "include/debug.hpp" ENDS HERE
	////////////////////////////////////////////////////////////////////////////////
	
	
	
	////////////////////////////////////////////////////////////////////////////////
	// AMALGAMATE: "include/abbrevs.hpp" BEGINS HERE
	//
		
		#define UI unsigned int
		
		#define LL long long
		#define ULL unsigned long long
		
		
		auto ri()   { int r; cin >> r; return r; }
		auto rui()  { UI r; cin >> r; return r; }
		
		auto rll()  { LL r;  cin >> r; return r; }
		auto rull() { ULL r; cin >> r; return r; }
		
		auto rstr() {string s; cin >> s; return s; }
		
		
		#define RI ri()
		#define RUI rui()
		
		#define RLL rll()
		#define RULL rull()
		
		#define RSTR rstr()
		
		
		
		#define FOR(i,n) for(int i=0; i<int(n); ++i)
		#define FO(i,a,b) for(int i=(a); i<int(b); ++i)
		#define OF(i,a,b) for(int i=(b)-1; i>=int(a); --i)
		
		
		
		#define MIN(a,b) ((a)<(b) ? (a) : (b))
		#define MAX(a,b) ((b)<(a) ? (a) : (b))
		
		#define REMIN(a,b) ((a) = min(a,b))
		#define REMAX(a,b) ((a) = max(a,b))
		
		#define ALL(c) (c).begin(),(c).end()
		
		#define SQR(x) ((x)*(x))
	
	//
	// AMALGAMATE: "include/abbrevs.hpp" ENDS HERE
	////////////////////////////////////////////////////////////////////////////////
	
	
	
	//
	// for salgo
	#define CONTEST_MODE
	
	namespace salgo {};
	using namespace salgo;
	//

//
// AMALGAMATE: "include/template.hpp" ENDS HERE
////////////////////////////////////////////////////////////////////////////////


//#include <salgo/graph.hpp> // c++17
//#include <salgo/binomial.hpp>
//#include <salgo/modulo.hpp>
//#include <salgo/common.hpp>


struct Test_Case {

	//int n = RI;
	//int m = RI;
	//int k = RI;


	void solve() {
		// cout << "Case #" << icase+1 << ": ";
		cout.precision(15);
		cout << fixed;

		int n = RI;
		int m = RI;

		LL result = 0;

		FOR(i,m) {
			int x=RI, d=RI;

			result += x*n;

			if(d>0) {
				result += 1LL * n * (n-1) / 2 * d;
			}
			else {
				result += 1LL * (n/2) * ((n-1)/2 + 1) * d;
			}

			//cerr << "current " << result << endl;
		}

		cout << 1.0L * result / n << endl;
	}

	int icase = -1;
}; // struct Test_Case



int main() {
	int num_cases = READ_NUM_TEST_CASES ? RI : 1;
	
	FOR(i, num_cases) {
		Test_Case tc;
		tc.icase = i;
		tc.solve();
	}

	return 0;
}