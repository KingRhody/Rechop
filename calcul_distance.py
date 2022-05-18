def calcul_distance(list):
    """Prend une liste d'indices en argument
    Commence par prendre le 2ème indice dans la liste (celui qui correspond à la première commune
    que le camion rejoint)"""
    distance = 0
    for i in range(1, len(list)):
        if i < len(list):
            distance += list[i][i-1]
        else :
            distance += list[i][0]
    return distance
