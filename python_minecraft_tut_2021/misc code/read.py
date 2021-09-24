import pickle

map=[]
with open('test.pycraft', 'r') as f:
    for line in f:                       # For each line
        map.append(list(line[:-1])) 

print(map)

with open('test.pycraft', 'a') as f:
    print(map, file=f)