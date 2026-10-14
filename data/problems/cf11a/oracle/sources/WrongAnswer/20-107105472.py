import sys
# import logging
# logging.root.setLevel(logging.INFO)

n,k = map(int,sys.stdin.readline().strip().split())
nums = list(map(int,sys.stdin.readline().strip().split()))
deltas = []

for pre,cur in zip(nums,nums[1:]):
    deltas.append(cur-pre)

times  = 0 
pre_delta = 0
for i,delta in enumerate(reversed(deltas)):
    if delta <= 0:
        to_positive =  (-delta//k)+1
        if to_positive*k >= pre_delta:
            times += to_positive * (i+1)
        else:
            times += to_positive
    pre_delta = delta


print(times)