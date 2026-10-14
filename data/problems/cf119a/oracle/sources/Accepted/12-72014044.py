from math import gcd

a, b, n = map(int, input().split())

remaining_stones = n
simons_turn = True
for i in range(n):
    if simons_turn:
        stones_to_remove = gcd(a, remaining_stones)
    else:
        stones_to_remove = gcd(b, remaining_stones)

    if stones_to_remove > remaining_stones:
        break

    # print('Simons turn: {}, Remaining stones: {}, Num stones to remove: {}'
    #       .format(simons_turn, remaining_stones, stones_to_remove))
    remaining_stones -= stones_to_remove
    simons_turn = not simons_turn

print(1 if simons_turn else 0)