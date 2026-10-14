def get_int_map(input_string):
    return map(int, input_string.split())

def is_free_places(places):
    for i in range(len(places)):
        if places[i] == 1:
            return False
    return True

def find_distance(center, row, column, places_count):
    return abs(row-center) + abs(column-center) + places_count-1

def berland_cinema(parameters, requests):
    request_count, cinema_size = get_int_map(parameters)
    requests_list = list(get_int_map(requests))
    cinema_room = [[0] * cinema_size for _ in range(cinema_size)]
    center = (cinema_size+1)/2
    result = list()

    for count in requests_list:
        row, y_left, y_right = 0, 0, 0
        min_dist = float('inf')
        for i in range(cinema_size):
            for j in range(cinema_size-count+1):
                if is_free_places(cinema_room[i][j:j+count]):
                    distance = find_distance(center, i, j, count)
                    if distance < min_dist:
                        min_dist = distance
                        row, y_left, y_right = i, j, j+count
        if min_dist == float('inf'):
            result.append("-1")
            continue

        for i in range(y_left, y_right):
            cinema_room[row][j] = 1
        result.append(f"{row+1} {y_left+1} {y_right}")
        
    return "\n".join(result)

parameters = input()
requests = input()

print(berland_cinema(parameters, requests))