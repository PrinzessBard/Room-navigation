coordinates = {}
with open("text1.txt", encoding="utf-8") as file:
    for line in file:
        key, *value = line.split()
        coordinates[key] = value

new_coordinates = {}
for key, item in coordinates.items():
    new_key = int(key)
    new_coordinates[new_key] = [[int(item[0]), int(item[1])], [int(item[2]), int(item[3])], [int(item[4]), int(item[5])], [int(item[6]), int(item[7])]]



for key, item in new_coordinates.items():
    print(item)
    for i in item:
        print(i) # (5, 10)
        if i[0] == 0 and i[1] == 0:
            print(i[0], "   ", i[1])
            item.remove(i) 
        else:
            pass


for key, item in new_coordinates.items():
    print(item)
    for i in item:
        print(i) # (5, 10)
        if i[0] == 0 and i[1] == 0:
            print(i[0], "   ", i[1])
            item.remove(i) 
        else:
            pass

 
return new_coordinates

# {'1:': ['[(5,', '10)]'], '2:': ['[(6,', '10)]']}
# {1: (5, 10), 2: (6, 10)}
# {1: [(5, 10), (0, 0), (0, 0), (0, 0)]}

# (5, 10)
# (0, 0)
# (0, 0)
# (0, 0)
# (6, 10)
# (0, 0)
# (0, 0)
# (0, 0)
