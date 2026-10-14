n, p1, p2, p3, t1, t2 = map(int, input().split())

total_power = 0
last_event_time = -1
last_event_type = 0

for i in range(n):
    l, r = map(int, input().split())
    
    total_power += p1 * (l - last_event_time - 1)
    
    if last_event_type == 0 or l - last_event_time > t2:
        total_power += (r - l + 1) * p1
    elif last_event_type == 1 or l - last_event_time > t1:
        total_power += t1 * p1 + (r - l + 1 - t1) * p2
    else:
        total_power += (l - last_event_time - 1) * p2 + (r - l + 1 - (l - last_event_time - 1)) * p3
    
    last_event_time = r
    last_event_type = 0
    
    if i < n-1 and r+1 != int(input().split()[0]):
        gap_time = int(input().split()[0]) - r - 1
        if last_event_type == 0 or gap_time > t2:
            total_power += t2 * p2
        elif last_event_type == 1 or gap_time > t1:
            total_power += t1 * p1 + (gap_time - t1) * p2
        else:
            total_power += gap_time * p3
        last_event_type = 2

total_power += p1 * (1440 - last_event_time)

print(total_power)