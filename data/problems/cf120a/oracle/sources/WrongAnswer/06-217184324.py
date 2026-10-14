# https://codeforces.com/problemset/problem/120/A

with open('input.txt') as input_file:
    door, rail = input_file.readlines()
    if ('front' in door and rail == '1') or ('back' in door and rail == '2'):
        result = 'L'
    else:
        result = 'R'

result_file = open("output.txt", "w+")
result_file.write(result)
result_file.close()