n = int(input())
laptops = []
for i in range(n):
    laptop_info = {}
    laptop = input()
    laptop = laptop.split()
    laptop_info['speed'] = laptop[0]
    laptop_info['ram'] = laptop[1]
    laptop_info['hdd'] = laptop[2]
    laptop_info['price'] = laptop[3]
    laptops.append(laptop_info)
min_speed = laptops[0]['speed']
min_ram = laptops[0]['ram']
min_hdd = laptops[0]['hdd']
max_price = laptops[0]['price']
for i in range(len(laptops)):
    if laptops[i]['speed'] <= min_speed:
        min_speed = laptops[i]['speed']
    if laptops[i]['ram'] <= min_ram:
        min_ram = laptops[i]['ram']
    if laptops[i]['hdd'] <= min_hdd:
        min_hdd = laptops[i]['hdd']
    if laptops[i]['price'] <= max_price:
        max_price = laptops[i]['price']
for i in range(len(laptops)):
    if laptops[i]['speed'] == min_speed and laptops[i]['ram'] == min_ram and laptops[i]['hdd'] == min_hdd:
        laptops[i]['price'] = max_price
min_price = max_price
for i in range(len(laptops)):
    if laptops[i]['price'] <= min_price:
        min_price = laptops[i]['price']
        min = i
print(min)