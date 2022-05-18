import random

f = open("distances.txt")
initial_distance_matrix = []
for line in f:
    distance_string = line.strip('\n').split(",")
    distance_float = [float(i) for i in distance_string]
    initial_distance_matrix.append(distance_float)

"print(initial_distance_matrix)"

matrix_path, c1_path, c2_path, c3_path, c1_index, c2_index, c3_index, = [], [], [], [], [0], [0], [0]
random_init_path = random.sample(range(1, 19), 3)
index_path_list = list(range(1, 20))


def generate_index_path(c_path_index_list, len_list):
    """Generation des indices de commune à traverser par un camion c"""
    while len(index_path_list) != 0 and len(c_path_index_list) != len_list:
        index = random.randint(0, len(index_path_list)-1)
        if index_path_list[index] not in random_init_path:
            c_path_index_list.append(index_path_list[index])
        index_path_list.remove(index_path_list[index])


def c_index_init():
    """Initialisation des indices de commune à traverser par les trois camions"""
    c1_index.append(random_init_path[0])
    c2_index.append(random_init_path[1])
    c3_index.append(random_init_path[2])

    generate_index_path(c1_index, 7)
    generate_index_path(c2_index, 7)
    generate_index_path(c3_index, 8)

    print(random_init_path)
    print(c1_index, c2_index, c3_index)


c_index_init()


def generate_dist_path():
    """length = len(initial_distance_matrix)
    for i in range(20):
        if (i not in random_init_path) and (len(c1_path)) < 6:
            c1_path.append(initial_distance_matrix[i][-2])
        elif (i not in random_init_path) and ((6 <= i < 2*len(c1_path)) or (len(c2_path) < 6)):
            c2_path.append(initial_distance_matrix[i][-2])
        elif (2*len(c1_path) <= i < length) and (i not in random_init_path):
            c3_path.append(initial_distance_matrix[i][-2])"""


def initial_path():
    """Genration des trajets entre la banque et 3 premieres communes"""

    c1_path.append(initial_distance_matrix[c1_index[1]][0])
    c2_path.append(initial_distance_matrix[c2_index[1]][0])
    c3_path.append(initial_distance_matrix[c3_index[1]][0])

    print(c1_path, c2_path, c3_path)


def fill_matrix_path():
    initial_path()
    matrix_path.append(c1_path)
    matrix_path.append(c2_path)
    matrix_path.append(c3_path)
    print(matrix_path)


"fill_matrix_path()"
