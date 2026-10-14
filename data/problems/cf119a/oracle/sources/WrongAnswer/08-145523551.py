from math import gcd


def main():
    a, b, n = list(map(int, input().split()))

    turn = 0
    while True:
        if turn == 0:
            turn = 1
        else:
            turn = 0
        to_take = gcd(n, a)
        n -= to_take
        if n < 0:
            print(turn)
            break


if __name__ == "__main__":
    main()