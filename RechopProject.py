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
    distance, risk = calculate_distance_risk(dist_foreach_path,risk_foreach_path)
    return distance, risk

def calculate_distance_risk(distance_list, risk_list):
    total_distance = 0
    total_risk = 0
    for i in range(3):
        total_distance += distance_list[i]
        total_risk += risk_list[i]

    return total_distance, total_risk


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
    return current_matrix_index


def generate_solution(current_matrix_index1, current_matrix_path1, current_matrix_index2, current_matrix_path2):
    """Genration des trajets entre la banque et 3 premieres communes"""
    matrix_index1 = c_index_init(current_matrix_index1)
    matrix_index2 = c_index_init(current_matrix_index2)
    distance1, risk1 = calculate_path_dist_risk(matrix_index1, current_matrix_path1)
    distance2, risk2 = calculate_path_dist_risk(matrix_index2, current_matrix_path2)
    print(distance2, risk2)
    print(distance1
          , risk1)
    if distance1 < distance2 and risk1 < risk2:
        best_distance, best_risk = distance1, risk1
    elif distance2 < distance1 and risk2 < risk1:
        best_distance, best_risk = distance2, risk2
    return best_distance, best_risk


matrix_index1 = [[], [], []]
matrix_index2 = [[], [], []]
matrix_path1 = [[], [], []]
matrix_path2 = [[], [], []]

print(generate_solution(matrix_index1, matrix_path1, matrix_index2, matrix_path2))
