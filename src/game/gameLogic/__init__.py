
def possible_moves(cords, cord_list_of_bottom_pieces, cord_list_of_top_pieces):
    return_dict = dict()
    if cords in cord_list_of_bottom_pieces:
        if (cords[0] - 1, cords[1] + 1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cords[0]-1 >= 0 and cords[1]+1 <= 7:
                return_dict[(cords[0] - 1, cords[1] + 1)] = 0

        if (cords[0] + 1, cords[1] + 1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cords[0]+1 <= 7 and cords[1]+1 <= 7:
                return_dict[(cords[0] + 1, cords[1] + 1)] = 0

    else:
        if (cords[0] - 1, cords[1] - 1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cords[0]-1 >= 0 and cords[1]-1 >= 0:
                return_dict[(cords[0] - 1, cords[1] - 1)] = 0

        if (cords[0] + 1, cords[1] - 1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cords[0]+1 <= 7 and cords[1]-1 >= 0:
                return_dict[(cords[0] + 1, cords[1] - 1)] = 0
    return return_dict


def possible_attacks(cords, cord_list_of_bottom_pieces, cord_list_of_top_pieces):
    if cords in cord_list_of_bottom_pieces:
        przeciwnik = cord_list_of_top_pieces
    else:
        przeciwnik = cord_list_of_bottom_pieces

    wszystkie = cord_list_of_bottom_pieces + cord_list_of_top_pieces
    return_dict = dict()
    if (cords[0] - 1, cords[1] + 1) in przeciwnik and (cords[0] - 2, cords[1] + 2) not in wszystkie:
        if cords[0] - 2 >= 0 and cords[1] + 2 <= 7:
            return_dict[(cords[0] - 2, cords[1] + 2)] = (cords[0] - 1, cords[1] + 1)

    if (cords[0] + 1, cords[1] + 1) in przeciwnik and (cords[0] + 2, cords[1] + 2) not in wszystkie:
        if cords[0] + 2 <= 7 and cords[1] + 2 <= 7:
            return_dict[(cords[0] + 2, cords[1] + 2)] = (cords[0] + 1, cords[1] + 1)

    if (cords[0] + 1, cords[1] - 1) in przeciwnik and (cords[0] + 2, cords[1] - 2) not in wszystkie:
        if cords[0] + 2 <= 7 and cords[1]-2 >= 0:
            return_dict[(cords[0] + 2, cords[1] - 2)] = (cords[0] + 1, cords[1] - 1)

    if (cords[0] - 1, cords[1] - 1) in przeciwnik and (cords[0] - 2, cords[1] - 2) not in wszystkie:
        if cords[0] - 2 >= 0 and cords[1] - 2 >= 0:
            return_dict[(cords[0] - 2, cords[1] - 2)] = (cords[0] - 1, cords[1] - 1)
    return return_dict
