def main():
    n, aa = int(input()), list(map(int, input().split()))
    res = sum(aa)
    for i, a in enumerate(aa):
        if a > 1:
            res += i
    print(res)


if __name__ == "__main__":
    main()