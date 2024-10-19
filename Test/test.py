import heapq
import jellyfish

def similar(first, second):
    first = first.replace(' ', '')
    second = second.replace(' ', '')
    # if len(first) - sum(l1==l2 for l1, l2 in zip(first, second)) > 5:
    #     return False
    # return True
    if jellyfish.levenshtein_distance(first, second) > 4:
        return False
    else:
        return True

def dijkstra(graph, start, goal):
    queue = [(0, start)]
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    previous_nodes = {vertex: None for vertex in graph}

    while queue:
        current_distance, current_vertex = heapq.heappop(queue)

        if current_distance > distances[current_vertex]:
            continue

        if current_vertex == goal:
            break

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(queue, (distance, neighbor))

    # Восстановление пути
    path = []
    current_node = goal
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    return path[::-1]  # возвращаем путь в обратном порядке


def graph_from_file(file):
    coordinates = {}
    with open(file, encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            coordinates[key] = value

    new_coordinates = {}
    for key, item in coordinates.items():
        new_key = int(key)
        new_coordinates[new_key] = [[int(item[0]), int(item[1])], [int(item[2]), int(item[3])], [int(item[4]), int(item[5])], [int(item[6]), int(item[7])]]



    for key, item in new_coordinates.items():
        for i in item:
            if i[0] == 0 and i[1] == 0:
                item.remove(i) 
            else:
                pass


    for key, item in new_coordinates.items():
        for i in item:
            if i[0] == 0 and i[1] == 0:
                item.remove(i) 
            else:
                pass

     
    return new_coordinates


def get_room_number(start_room, end_room, address, room_level, d):
    def remove_commas(string):
        trans_table = {ord('[') : None, ord(']') : None, ord('\'') : None}
        return string.translate(trans_table)

    if end_room != "":

        d = {}
        with open(f"/home/egor/Work/Room-navigation/building/school_3/text/text_level_1.txt", encoding="utf-8") as file:
            for line in file:
                key, *value = line.split()
                d[key] = value

        start_room_number = 0
        end_room_number = 0

        for key, item in d.items():
            x = remove_commas(str(item))
            new_item = x.replace("_", " ")
            test = similar(start_room, new_item)
            if start_room == new_item:
                start_room_number = key
            elif test == True:
                start_room_number = key
            else:
                continue


        for key, item in d.items():
            x = remove_commas(str(item))
            new_item = x.replace("_", " ")
            test = similar(end_room, new_item)
            if end_room == new_item:
                end_room_number = key
            elif test == True:
                end_room_number = key
            else:
                continue


        return int(start_room_number), int(end_room_number)

    else:
        start_room_number = 0

        for key, item in d.items():
            x = remove_commas(str(item))
            new_item = x.replace("_", " ")
            test = similar(start_room, new_item)
            if start_room == new_item:
                start_room_number = key
            elif test == True:
                start_room_number = key
            else:
                continue

        return int(start_room_number)


# def checking_nearby_points(file, start, room_level, name):


#     def val(num, her):
#         ok = her.index(num) + 1
#         if ok == len(her):
#             return False
#         else:
#             number = her[(her.index(num) + 1)]
#             return number



#     def get_summa_p(start, end, address, room_level):
#         graph = graph_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/level_{room_level}/graph.txt')

#         summa = 0
#         her = dijkstra(graph, start, end)

#         for i in her:
#             for j in graph[i]:
#                 hui = val(i, her)
#                 if hui == False:
#                     break
#                 else:
#                     if hui != j[0]:
#                         continue
#                     else:
#                         summa = summa + j[1]

#         return summa


#     d = {}
#     with open(f"/home/egor/Work/Room-navigation/building/school_3/text/text_level_1.txt", encoding="utf-8") as file:
#         for line in file:
#             key, *value = line.split()
#             d[key] = value

#     value = {}

#     while True:
#         try:
#             test = get_room_number("столовая", "", "", "", d)
#             value[test] =  test
#             del d[str(test)]
#         except KeyError:
#             break

#     del value[0]

#     summa = {}

#     for key, item in value.items():
#         summa[key] = get_summa_p(item, 12, "school_3", 1)

#     minimal = 1000

#     for key, item in summa.items():
#         if minimal > item:
#             minimal = key
#         else:
#             continue


#     return minimal


def checking_nearby_points(start, end, room_level, address):

    # start, end = get_room_number(start, end, address, room_level)
    def val(num, her):
        ok = her.index(num) + 1
        if ok == len(her):
            return False
        else:
            number = her[(her.index(num) + 1)]
            return number



    def get_summa_p(start, end, address, room_level):
        graph = graph_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/level_{room_level}/graph.txt')

        summa = 0
        her = dijkstra(graph, start, end)

        for i in her:
            for j in graph[i]:
                hui = val(i, her)
                if hui == False:
                    break
                else:
                    if hui != j[0]:
                        continue
                    else:
                        summa = summa + j[1]

        # print(summa)

        return summa


    d = {}
    with open(f"/home/egor/Work/Room-navigation/building/{address}/text/text_level_{room_level}.txt", encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            d[key] = value

    value = {}

    while True:
        try:
            test = get_room_number("лестница", "", "", "", d)
            value[test] =  test
            del d[str(test)]
        except KeyError:
            break

    del value[0]

    summa = {}

    for key, item in value.items():
        summa[key] = get_summa_p(item, 28, "school_3", 1)

    minimal = 1000

    for key, item in summa.items():
        if minimal > item:
            minimal = key
        else:
            continue


    return minimal


    
# print(checking_nearby_points("", "", 1, "school_3"))

for i in range(1, 3):
    print(i)
