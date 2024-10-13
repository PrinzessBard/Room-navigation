def similar(first, second):
    first = first.replace(' ', '')
    second = second.replace(' ', '')
    # if not len(first) == len(second):
    #     return False
    if len(first) - sum(l1==l2 for l1, l2 in zip(first, second)) > 3:
        return False
    return True

# def create_table(data, header_separator=True):

#     header_cols = len(data[0])

#     # Сделал чтобы строки "Категории" и "Цена", вывводились
#     # в качестве заголовка
#     elem_col1 = [data[0][0]] + list(data[1].keys())
#     elem_col2 = [data[0][1]] + list(map(str, list(data[1].values())))

#     # Определяет ширину для каждого столбика

#     col_width = [len(max(elem_col1, key=len)),
#                  len(max(elem_col2, key=len))]

#     # Границы заголовков столбцов
#     separator = "-+-".join('-' * n for n in col_width)

#     # Создание таблицы
#     i = 0
#     for col in range(len(elem_col1)):
#         if i == 1:
#             print(separator)
#         result = [elem_col1[col].rjust(col_width[0]),
#                   elem_col2[col].rjust(col_width[1])]
#         i += 1
#         print(" | ".join(result))


def test(start_room_name, end_room_name):
    def remove_commas(string):
        trans_table = {ord('[') : None, ord(']') : None, ord('\'') : None}
        return string.translate(trans_table)

    d = {}
    with open("text1.txt", encoding="utf-8") as file:
        for line in file:
            key, *value = line.split()
            d[key] = value


    # print(d)

    # start_room = input()
    # end_room = input()

    start_room_number = 0
    end_room_number = 0

    for key, item in d.items():
        x = remove_commas(str(item))
        new_item = x.replace("_", " ")
        test = similar(start_room_name, new_item)
        if start_room_name == new_item:
            start_room_number = key
        elif test == True:
            start_room_number = key
        else:
            continue


    for key, item in d.items():
        x = remove_commas(str(item))
        new_item = x.replace("_", " ")
        test = similar(end_room_name, new_item)
        if end_room_name == new_item:
            end_room_number = key
        elif test == True:
            end_room_number = key
        else:
            continue
    
    # data = [
    #     ["Номер", "Название"],
    #     {}
    # ]

    # for key, item in d.items():
    #     x = remove_commas(str(item))
    #     new_item = x.replace("_", " ")
    #     data[1][key] = new_item
    
    # print(create_table(data))
    # print(data)

    return start_room_number, end_room_number


start_room, end_room = test("Кажинет директора", "Мазыка")
print(start_room, end_room)

# print(similar("кабинет директора", "кабинетдиректора"))