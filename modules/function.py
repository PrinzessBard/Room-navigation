import sys
sys.path.append('egor@egor-laptop:~/Work/Room-navigation')

import cv2
import numpy as np
import heapq
import os
import jellyfish


# Алгоритм Дейкстера для нахождения кратчайшего пути по графу
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


# Функция для отрисовки маршрута на карте
def draw_path_on_map(image, path, coordinates):
    for i in range(len(path) - 1):
        start_room = path[i]
        end_room = path[i+1]
        start_coord = coordinates[start_room]
        end_coord = coordinates[end_room]
        # Отрисовка линии на изображении карты между двумя точками
        cv2.line(image, start_coord, end_coord, (0, 255, 0), 3)  # красная линия, толщина 3
    return image


# Функция для сравнения значений и нахождения различий и сходств
def similar(first, second):
    first = first.replace(' ', '')
    second = second.replace(' ', '')
    if jellyfish.levenshtein_distance(first, second) > 4:
        return False
    else:
        return True


# Функция для сравнения значений и нахождения различий и сходств ПАПОК в иерархии файлов
def similar_folder(word, list_dir):
    result = [] 
    for i in list_dir:
        result.append(jellyfish.levenshtein_distance(word, i))

    min_num = result[0]
    min_number_in_result = 0

    for i in range(len(result)):
        if min_num > result[i]:
            min_num = result[i]
            min_number_in_result = i
        else:
            continue

    if min_num > 3:
        return False
    else:
        return list_dir[min_number_in_result]


# Функция для получения словаря графа из файла
def graph_from_file(file):
    graph = {}
    with open(file, encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            graph[key] = value

    new_graph = {}
    for key, item in graph.items():
        new_key = int(key)
        new_graph[new_key] = [[int(item[0]), int(item[1])], [int(item[2]), int(item[3])], [int(item[4]), int(item[5])], [int(item[6]), int(item[7])]]



    for key, item in new_graph.items():
        for i in item:
            if i[0] == 0 and i[1] == 0:
                item.remove(i) 
            else:
                pass


    for key, item in new_graph.items():
        for i in item:
            if i[0] == 0 and i[1] == 0:
                item.remove(i) 
            else:
                pass

     
    return new_graph


# Функция для получения словаря координат из файла
def coordinates_from_file(file):
    coordinates = {}
    with open(file, encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            coordinates[key] = value

    new_coordinates = {}
    for key, item in coordinates.items():
        new_key = int(key)
        new_coordinates[new_key] = (int(item[0]), int(item[1]))

    return new_coordinates


# Функция для нахождения номера помещений из файла-перечня
def get_room_number(start_room, end_room, address, room_level, d):
    def remove_commas(string):
        trans_table = {ord('[') : None, ord(']') : None, ord('\'') : None}
        return string.translate(trans_table)

    if end_room != "" and start_room != "":
        d = {}
        with open(f"/home/egor/Work/Room-navigation/building/{address}/text/text_level_{room_level}.txt", encoding="utf-8") as file:
            for line in file:
                key, *value = line.split()
                d[key] = value

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

    elif start_room == "":
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

        return int(end_room_number)

    elif end_room == "":
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


# Функция для проверки одинаковых значений по словарб и нахождению ближайшего к пользователю
def checking_nearby_points(start, end, room_level, address):

    # start, end = get_room_number(start, end, address, room_level)
    def val(i, array_points):
        point_pos = array_points.index(i) + 1
        if point_pos == len(array_points):
            return False
        else:
            number = array_points[(array_points.index(i) + 1)]
            return number



    def get_summa_p(start, end, address, room_level):
        graph = graph_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/level_{room_level}/graph.txt')

        summa = 0
        array_points = dijkstra(graph, start, end)

        for i in array_points:
            for j in graph[i]:
                hui = val(i, array_points)
                if hui == False:
                    break
                else:
                    if hui != j[0]:
                        continue
                    else:
                        summa = summa + j[1]

        return summa


    d = {}
    with open(f"/home/egor/Work/Room-navigation/building/{address}/text/text_level_{room_level}.txt", encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            d[key] = value


    end = get_room_number(end, "", address, room_level, d)

    value = {}

    while True:
        try:
            test = get_room_number(start, "", address, room_level, d)
            value[test] =  test
            del d[str(test)]
        except KeyError:
            break

    del value[0]

    summa = {}

    for key, item in value.items():
        summa[key] = get_summa_p(item, end, address, room_level)

    minimal = 1000

    for key, item in summa.items():
        if minimal > item:
            minimal = key
        else:
            continue


    return minimal


# Функция для сохранения изображение в файловую систему
def save_image(address, room_level,  start_room_name, end_room):
    d = {}
    with open(f"/home/egor/Work/Room-navigation/building/{address}/text/text_level_{room_level}.txt", encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            d[key] = value

    graph = graph_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/level_{room_level}/graph.txt')
    coordinates = coordinates_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/level_{room_level}/coordinates.txt')
    image = cv2.imread(f'/home/egor/Work/Room-navigation/building/{address}/image/level_{room_level}.jpg')

    if isinstance(end_room, int): 
        start_room = get_room_number(start_room_name, "", address, room_level, d)
        path = dijkstra(graph, start_room, end_room)

    elif isinstance(start_room_name, int):
        end_room = get_room_number("", end_room, address, room_level, d)
        path = dijkstra(graph, start_room_name, end_room)

    else:
        start_room, end_room = get_room_number(start_room_name, end_room, address, room_level, {})
        path = dijkstra(graph, start_room, end_room)

    
    result_image = draw_path_on_map(image, path, coordinates)

    output_file = f'building/{address}/image/level_path_{room_level}.png'
    cv2.imwrite(output_file, result_image)
    os.system(f'xdg-open {output_file}') 


# Функция для проверки объекта в файле
def check_in_list(name, file):
    d = {}
    with open(file, encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            d[key] = value

    for key, item in d.items():
        item = item.lower()
        if name == item:
            return True
        else:
            continue

    return False


# Функция для обработки данных пользователя и выполнения отсльных функций (основная функция)
def processing_data_user_and_image():
    building_dir = os.listdir("/home/egor/Work/Room-navigation/building/")
    print(building_dir)

    address_name = input("Введите адрес здания: ")

    address = ""
    if similar_folder(address_name, building_dir) != False:
        address = similar_folder(address_name, building_dir)
    else:
        return 0

    image_dir = os.listdir(f"/home/egor/Work/Room-navigation/building/{address}/image")

    if len(image_dir) > 1:
        start_room_name = input("Введите название начальной комнаты: ").lower()
        start_room_level = int(input("Введите номер этажа первой комнаты: "))
        end_room_name = input("Введите название конечной комнаты: ").lower()
        end_room_level = int(input("Введите номер этажа второй комнаты: "))
        is_ladder = input("Какой вид смены этажей у вас(лифт, лестница): ").lower()

        if similar(is_ladder, "лифт") == True:
            is_ladder == "лифт"
        elif similar(is_ladder, "лестница") == True:
            is_ladder == "лестница"
        else:
            return 0


        if start_room_level != end_room_level:
            for i in range(1, 3):
                if i == 1:
                    # test = checking_nearby_points("лестница", start_room_name, start_room_level, address)
                    # print(test)
                    save_image(address, start_room_level,  start_room_name, checking_nearby_points(is_ladder, start_room_name, start_room_level, address))
                else:
                    save_image(address, end_room_level,  checking_nearby_points(is_ladder, start_room_name, start_room_level, address), end_room_name)
        else:
            save_image(address, start_room_level, start_room_name, end_room_name)

    else:
        start_room_name = input("Введите название начальной комнаты: ").lower()
        end_room_name = input("Введите название конечной комнаты: ").lower()

        save_image(address, 1, start_room_name, end_room_name)

