import sys
sys.path.append('C:/Users/user/Lodestar/python')

import cv2
import heapq
import os
import modules.linedata as ln
from modules.function import dijkstra, draw_path_on_map, test

# Основная функция
def main(start_room_name, end_room_name):
    graph = ln.get_graph()
    coordinates = ln.get_coordinates()

    # Загрузка карты здания (изображение)
    image = cv2.imread('image/scheme_school_2.jpg')

    try:
        start_room_name = input("Введите название начальной комнаты: ").lower()
        end_room_name = input("Введите название конечной комнаты: ").lower()

        start_room, end_room = test(start_room_name, end_room_name)

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
        output_file = 'image/building_map_with_path.png'
        cv2.imwrite(output_file, result_image)
        print(f"Изображение сохранено как {output_file}")
        os.system(f"{output_file}")
    
    except ValueError as e:
        print(e)

    return output_file


if __name__ == "__main__":
    main()