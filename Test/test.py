import jellyfish

def similar(word, list_dir):
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



list_dir = ['school_3', 'Bolkhov, Apuhtina', "Bolkhov, Gimnasia", "Bolkhov, Nekrasova"]

print(similar("Bolkhov Gimnas", list_dir))