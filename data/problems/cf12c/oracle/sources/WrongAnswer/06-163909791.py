if __name__ == '__main__':
    n, m = map(int, input().split())
    arr = [int(x) for x in input().split()]
    d = {}
    k = []
    for i in range (m):
        key = input()
        if key in d:
            d[key] += 1
        else:
            d[key] = 1
            k.append(key)
    value = []
    for i in range(len(k)):
        value.append(d[k[i]])
    value.sort(reverse=True)
    print(value)
    min_price = 0
    max_price = 0

    arr.sort()

    for i in range (len(k)):
        min_price += arr[i] * value[i]
        max_price += arr[len(arr) - 1 - i] * value[i]
    print(min_price, max_price)