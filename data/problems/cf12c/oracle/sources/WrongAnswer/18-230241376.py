def main():
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    fruits = []
    for i in range(m):
        fruits.append(input())

    prices.sort(reverse=True)

    min_sum = 0
    max_sum = 0
    for i in range(m):
        if fruits[i] in prices:
            min_sum += prices[min(i, m - i - 1)]
            max_sum += prices[max(i, m - i - 1)]
        else:
            min_sum += prices[0]
            max_sum += prices[-1]

    print(min_sum, max_sum)

if __name__ == '__main__':
    main()