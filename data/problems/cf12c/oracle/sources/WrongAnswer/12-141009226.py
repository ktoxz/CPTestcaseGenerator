case_list = input().split()
price_list = [*map(lambda x: int(x), input().split())]
fruit_list = [input() for i in range(int(case_list[1]))]
desc_price = sorted(price_list, reverse=True)  
asc_price = sorted(price_list)


def price_finder(price_list, fruit_list):
    duplicate_fruits = list(set([i for i in fruit_list if fruit_list.count(i) > 1]))
    duplicate_counts = sorted([fruit_list.count(i) for i in duplicate_fruits], reverse=True)
    included_price = price_list[len(duplicate_counts):len(fruit_list) - len(duplicate_counts)]
    included_price_dups = price_list[:len(duplicate_counts)]
    zipped = list(zip(duplicate_counts, included_price_dups))
    zipped_cost = [*map(lambda x: x[0] * x[1], zipped)]
    price = sum(zipped_cost) + sum(included_price)
    return price

    
max_price = price_finder(desc_price, fruit_list)
min_price = price_finder(asc_price, fruit_list)
print(str(min_price) + ' ' + str(max_price))