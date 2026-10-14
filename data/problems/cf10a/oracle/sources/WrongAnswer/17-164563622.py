n, p1, p2, p3, t1, t2 = map(int, input().split())

total_consumption = 0
prev = None
for _ in range(n):
    l, r = map(int, input().split())

    print(f"(l, r, total_consumption): {(l, r, total_consumption)}")

    if prev:
        if l - prev < t1:
            total_consumption += (l - prev) * p1
        elif t1 <= l - prev < t2:
            total_consumption += t1 * p1 + (l - prev - t1) * p2
        elif t2 <= l - prev:
            total_consumption += t1 * p1 + t2 * p2 + (l - prev - t1 - t2) * p3

    total_consumption += (r - l) * p1
    prev = r

print(total_consumption)