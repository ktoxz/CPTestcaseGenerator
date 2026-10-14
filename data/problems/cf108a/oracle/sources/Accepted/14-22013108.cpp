#include <iostream>

using namespace std;

void Mood();

void tel(int, char, int);

void tel2(int, char, int);

int main()

{

	Mood();

/////////////	system("pause");

	return 0;

}

void Mood()

{

	char sign;

	int hour, min;

	cin >> hour >> sign >> min;

	if (hour == 23 && min == 59)

		cout << "00" << sign << "00" << endl;

	else if (hour>=10)

	{

		tel(hour, sign, min);

	}

	else if (hour>=0&&hour<=9)

	{

		tel2(hour, sign, min);

	}

}

void tel(int hour, char sign, int min)

{



	int h,rev=0,m=hour;

	while (true)

	{

		h = hour;

		while (h != 0)

		{

			int d;

			d = h % 10;

			rev = (rev * 10) + d;

			h /= 10;

		}

		if (rev < 59)

		{

			if (m == hour&&rev <= min)

			{

                 //hour++;

				continue;

			}

			if (hour>23)

				cout << "00" << sign << "00" << endl;

			else if (rev < 10)

				cout << hour << sign << 0 << rev << endl;

			else

				cout << hour << sign << rev << endl;

			break;

		}

		rev = 0;

		hour++;

	}

}

void tel2(int hour, char sign, int min)

{

	int h, rev = 0,m;

	m = hour;

	if (hour == 0)

	{

		cout << "01" << sign << "10" << endl;

	}

	else

	{

		while (true)

		{

			h = hour;

			while (h != 0)

			{

				int d = h % 10;

				rev = 10 * d;

				h /= 10;

			}

			if (rev < 59)

			{

				if (m == hour&&rev <= min)

				{

					hour++;

					continue;

				}

				if (hour <= 9)

				{

					cout << 0 << hour << sign << rev << endl;

					break;

				}

				else

				{

					cout << "10" << sign << "01" << endl;

					break;

				}

			}

			rev = 0;

			hour++;

		}

	}

}