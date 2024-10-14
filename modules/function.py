import sys
sys.path.append('egor@egor-laptop:~/Work/Room-navigation')

import cv2
import numpy as np
import heapq
import os


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
    # if not len(first) == len(second):
    #     return False
    if len(first) - sum(l1==l2 for l1, l2 in zip(first, second)) > 3:
        return False
    return True


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
        # print(item)
        for i in item:
            # print(i) # (5, 10)
            if i[0] == 0 and i[1] == 0:
                # print(i[0], "   ", i[1])
                item.remove(i) 
            else:
                pass


    for key, item in new_coordinates.items():
        # print(item)
        for i in item:
            # print(i) # (5, 10)
            if i[0] == 0 and i[1] == 0:
                # print(i[0], "   ", i[1])
                item.remove(i) 
            else:
                pass

     
    return new_coordinates



def coordinates_from_file(file):
    old_dict = {}
    with open(file, encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            old_dict[key] = value

    new_dict = {}
    for key, item in old_dict.items():
        new_key = int(key)
        new_dict[new_key] = (int(item[0]), int(item[1]))

    return new_dict


# Функция для нахождения номера помещений из файла-перечня
def test(start_room, end_room, address):
    def remove_commas(string):
        trans_table = {ord('[') : None, ord(']') : None, ord('\'') : None}
        return string.translate(trans_table)


    d = {}
    with open(f"/home/egor/Work/Room-navigation/building/{address}/text/text.txt", encoding="utf-8") as file:
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


def processing_data_user_and_image():
    start_room_name = input("Введите название начальной комнаты: ").lower()
    end_room_name = input("Введите название конечной комнаты: ").lower()
    address = input("Введите адреса здания: ")

    graph = graph_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/graph.txt')
    coordinates = coordinates_from_file(f'/home/egor/Work/Room-navigation/building/{address}/graph/coordinates.txt')

    # Загрузка карты здания (изображение)
    image = cv2.imread(f'/home/egor/Work/Room-navigation/building/{address}/image/level_1.jpg')#

    start_room, end_room = test(start_room_name, end_room_name, address)

    if start_room not in graph:
        raise ValueError(f"Комната {start_room} отсутствует в графе.")
    if end_room not in graph:
        raise ValueError(f"Комната {end_room} отсутствует в графе.")

    # Поиск кратчайшего пути
    path = dijkstra(graph, start_room, end_room)
    print(f"Кратчайший путь: {path}")

    # Отрисовка пути на карте
    result_image = draw_path_on_map(image, path, coordinates)

    # Сохранение результата
    output_file = 'building/school_3/image/building_map_with_path.png'
    cv2.imwrite(output_file, result_image)
    # print(f"Изображение сохранено как {output_file}")
    # os.system(f"{output_file}")
