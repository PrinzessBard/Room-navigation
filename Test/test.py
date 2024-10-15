def similar(first, second):
    first = first.replace(' ', '')
    second = second.replace(' ', '')
    if len(first) - sum(l1==l2 for l1, l2 in zip(first, second)) > 3:
        return False
    return True


def check_list_dir(list_dir, address):
    for i in list_dir:
        if similar(address, i) == True:
            return i
        else:
            continue
    return False


list_dir = ['school_3', 'Bolkhov, Apuhtina']

print(check_list_dir(list_dir, 'Bolkhov, Apuhtin'))