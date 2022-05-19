import random

f = open("distances.txt")
initial_distance_matrix = []
for line in f:
    distance_string = line.strip('\n').split(",")
    distance_float = [float(i) for i in distance_string]
    initial_distance_matrix.append(distance_float)

"print(initial_distance_matrix)"

amount_list = [84975.8, 24455.9, 17701.6, 131380.2,
               33756.1, 30436.7, 39389.7, 17641.4, 60841.9,
               36822.8, 15397.9, 67971.4, 33948.6, 18766.3,
               91189, 59252.9, 17633, 40913.6, 29474.2]


def generate_index_path(c_path_index_list, len_list, index_path_list):
    """Generation des indices de commune à traverser par un camion c"""
    c_path_index_list.append(0)
    while len(index_path_list) != 0 and len(c_path_index_list) != len_list:
        index = random.randint(0, len(index_path_list) - 1)
        c_path_index_list.append(index_path_list[index])
        index_path_list.remove(index_path_list[index])
    c_path_index_list.append(0)


def calculate_path_dist_risk(all_index_list, current_matrix_path):
    """Generation d'une matrice de distances entre les communes traversees par les trois camions
    + calcul de la distance total de chaque camion et le risque correspondant"""
    current_index = 0
    dist_foreach_path, risk_foreach_path = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]

    for i in all_index_list:
        c = 0
        while c < len(i) - 1:
            get_distance = initial_distance_matrix[max(i[c], i[c + 1])][min(i[c], i[c + 1])]
            current_matrix_path[current_index].append(get_distance)
            dist_foreach_path[current_index] += get_distance
            if c != 0 and c < len(i)-1 and i[c] < 19:
                risk_foreach_path[current_index] += get_distance * amount_list[i[c]]
            c += 1
        current_index += 1
    print(dist_foreach_path)
    print(risk_foreach_path)
    return None


def get_total_distance(dist_list):
    total_distance = 0
    for i in dist_list:
        total_distance += i
    return total_distance


def c_index_init(current_matrix_index):
    """Initialisation des indices de commune à traverser par les trois camions"""
    index_path_list = list(range(1, 20))
    len_list1, len_list2, len_list3 = 7, 7, 8
    generate_index_path(current_matrix_index[0], len_list1, index_path_list)
    generate_index_path(current_matrix_index[1], len_list2, index_path_list)
    generate_index_path(current_matrix_index[2], len_list3, index_path_list)
    print(matrix_index)


def generate_solution(current_matrix_index, current_matrix_path):
    """Genration des trajets entre la banque et 3 premieres communes"""
    c_index_init(current_matrix_index)
    calculate_path_dist_risk(current_matrix_index, current_matrix_path)
    print(matrix_path)


matrix_index = [[], [], []]
matrix_path = [[], [], []]

generate_solution(matrix_index, matrix_path)
