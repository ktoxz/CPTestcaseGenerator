precision = 1000000
num_of_planets = int(input())
payload = int(input())*precision

takeoffs = list(map(int, input().split()))
landings = list(map(int, input().split()))

planets = []

for x in range(num_of_planets):
    a, b = takeoffs[x], landings[x]  # weight *precision / weight *precision
    planets.append([a, b]) # 0: lift-off, 1: land

def Calculate(fuel):
    weight = payload + fuel
    left_fuel = fuel
    earth=planets[0]

    takeoff = earth[0]
    burned_fuel=weight/takeoff
    left_fuel = left_fuel - burned_fuel
    weight = payload + left_fuel
    # check here
    if left_fuel<0:
        return False 
        
    for x in planets[1:]:
        #landing 
        landing = x[1]
        burned_fuel = weight/landing
        left_fuel = left_fuel - burned_fuel
        weight = payload + left_fuel
        # check here
        if left_fuel<0:
            return False 
      
        #takeoff
        takeoff = x[0]
        burned_fuel = weight/takeoff
        left_fuel = left_fuel - burned_fuel
        weight = payload + left_fuel
        # check here
        if left_fuel<0:
            return False 
      
    landing = earth[1]
    burned_fuel=weight/landing
    left_fuel = left_fuel - burned_fuel
    weight = payload + left_fuel
    # check here
    if left_fuel<0:
        return False 
    return True   
    
min_fuel = 1*precision
max_fuel = 1000000000*precision

while (max_fuel>min_fuel):
  mid=(min_fuel+max_fuel)//2

  #print("Before: [", min_fuel,",", max_fuel,"] -> midpoint: ", mid)

  if (Calculate(mid)):
    # update interval
    max_fuel=mid
  else:
    # update interval
    min_fuel=mid+1

  # old midpoint
  # min and max is new
  #print("After: [", min_fuel,",", max_fuel,"]")

# Here:
if Calculate(min_fuel):
  answer = min_fuel/precision
else:
  answer = -1

print(answer)