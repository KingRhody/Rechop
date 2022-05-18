import random

f = open("distances.txt")
initial_distance_matrix = []
for line in f:
    distance_string = line.strip('\n').split(",")
    distance_float = [float(i) for i in distance_string]
    initial_distance_matrix.append(distance_float)

"print(initial_distance_matrix)"

matrix_index, c1_path, c2_path, c3_path,  c1_index, c2_index, c3_index = [], [], [], [], [0], [0], [0]
matrix_path = [c1_path, c2_path, c3_path]
random_init_path = random.sample(range(1, 20), 3)
index_path_list = list(range(1, 20))


def generate_index_path(c_path_index_list, len_list):
    """Generation des indices de commune à traverser par un camion c"""
    while len(index_path_list) != 0 and len(c_path_index_list) != len_list:
        index = random.randint(0, len(index_path_list)-1)
        if index_path_list[index] not in random_init_path:
            c_path_index_list.append(index_path_list[index])
        index_path_list.remove(index_path_list[index])
    matrix_index.append(c_path_index_list)


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
            "risk_foreach_path[current_index] += get_distance*money_list[current_index]"
            c += 1
        current_index += 1
    print(dist_foreach_path)


def get_total_distance(dist_list):
    total_distance = 0
    for i in dist_list:
        total_distance += i
    return total_distance


def c_index_init():
    """Initialisation des indices de commune à traverser par les trois camions"""
    c1_index.append(random_init_path[0])
    c2_index.append(random_init_path[1])
    c3_index.append(random_init_path[2])

    generate_index_path(c1_index, 7)
    generate_index_path(c2_index, 7)
    generate_index_path(c3_index, 8)

    print(random_init_path)
    print(matrix_index)


def initial_path():
    """Genration des trajets entre la banque et 3 premieres communes"""
    c_index_init()
    calculate_path_dist_risk(matrix_index, matrix_path)
    print(matrix_path)


initial_path()
