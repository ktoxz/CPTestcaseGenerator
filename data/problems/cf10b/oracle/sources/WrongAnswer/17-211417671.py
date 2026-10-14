N, K = map(int, input().split())
requests = list(map(int, input().split()))

for M in requests:
    min_distance = float('inf')
    chosen_seat = None
    for row in range(1, K + 1):
        if row + M - 1 <= K:
            distance = abs(row + M // 2 - (K + 1) // 2)
            if distance < min_distance or (distance == min_distance and row < chosen_seat):
                min_distance = distance
                chosen_seat = row

    if chosen_seat is None:
        print(-1)
    else:
        print(chosen_seat, chosen_seat + M - 1 - (1 if M % 2 == 0 else 0), chosen_seat + M - 1)