#include <iostream>

#include <string>

#include <vector>



using namespace std;



int is_adj (string& s) {

	if (s.length() < 4) return 0;

	if (s.substr (s.length()-4, 4) == "lios") return 1;

	if (s.length() < 5) return 0;

	if (s.substr (s.length()-5, 5) == "liala") return 2;

	return 0;

}



int is_noun (string& s) {

	if (s.length() < 3) return 0;

	if (s.substr (s.length()-3, 3) == "etr") return 1;

	if (s.length() < 4) return 0;

	if (s.substr (s.length()-4, 4) == "etra") return 2;

	return 0;

}



int is_verb (string& s) {

	if (s.length() < 6) return 0;

	if (s.substr (s.length()-6, 6) == "initis") return 1;

	if (s.substr (s.length()-6, 6) == "inites") return 2;

	return 0;

}



int valid (string& s) {

	return is_noun (s) | is_adj(s) | is_verb (s);

}



int main() {

	// your code goes here

//	freopen ("in.txt", "r", stdin);

	vector<string> v;

	string s;

	int gender = 0;

	int state = -1;

	while (cin >> s) {

		v.push_back (s);

	}

	if (v.size() == 1) {

		if (valid (v[0])) cout<<"YES\n";

		else cout<<"NO\n";

		return 0;

	}

	for (int i=0; i<v.size(); i++) {

		s = v[i];

		int n_gender = valid (s);

		if (!n_gender) {

			cout<<"NO\n";

			return 0;

		}

		if (gender == 0) gender = n_gender;

		else if (n_gender != gender) {

			cout<<"NO\n";

			return 0;

		}

		int cur_word = 0;

		if (is_adj(s)) cur_word = 0;

		else if (is_noun(s)) cur_word = 1;

		else cur_word = 2;

		if (cur_word < state || (state == 1 && cur_word == 1) || ( (state == 0 || state == -1) && cur_word == 2)) {

			cout<<"NO\n";

			return 0;

		}

		state = cur_word;

	}

	if (state == 0) cout<<"NO\n";

	else cout<<"YES\n";

	return 0;

}