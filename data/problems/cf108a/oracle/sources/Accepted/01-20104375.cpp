#include<iostream>

using namespace std;

int main () {

    int a,b,d=0;

    char s;

    cin >> a >> s >> b;

    a = (a * 100) + (10 * (b / 10 % 10) ) + b % 10;

    if(a < 110)

    cout << "01:10";

    else if(a < 220)

    cout << "02:20";

    else if(a < 330)

    cout << "03:30";

    else if(a < 440)

    cout << "04:40";

    else if(a < 550)

    cout << "05:50";

    else if(a < 1001)

    cout << "10:01";

    else if(a < 1111)

    cout <<"11:11";

    else if(a < 1221)

    cout << "12:21";

    else if(a < 1331)

    cout << "13:31";

    else if(a < 1441)

    cout << "14:41";

    else if(a < 1551)

    cout << "15:51";

    else if(a < 2002)

    cout << "20:02";

    else if(a < 2112)

    cout << "21:12";

    else if(a < 2222)

    cout << "22:22";

    else if(a < 2332)

    cout << "23:32";

    else

    cout<<"00:00";	

	return 0;

}