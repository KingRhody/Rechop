import random

index_list = list(range(0, 19))

f = open("distances.txt")
initial_distance_matrix = []
for line in f:
    distance_string = line.strip('\n').split(",")
    distance_float = [float(i) for i in distance_string]
    initial_distance_matrix.append(distance_float)

"print(initial_distance_matrix)"

matrix_path, c1_path, c2_path, c3_path = [], [], [], []
random_numbers = random.sample(range(1, 20), 3)
random_init_path = [random_numbers[0], random_numbers[1], random_numbers[2]]


def first_path():
    """Genration des trajets entre la banque et les 3 premieres communes"""
    c1_path.append(initial_distance_matrix[random_init_path[0]][0])
    c2_path.append(initial_distance_matrix[random_init_path[1]][0])
    c3_path.append(initial_distance_matrix[random_init_path[2]][0])
    print(random_numbers)
    print(c1_path, c2_path, c3_path)


def initial_path():
    """Genration des trajets de chaque camion dans une matrice"""
    first_path()
    i = 1
    length = len(initial_distance_matrix)
    while i < 20:
        if (i not in random_init_path) and (len(c1_path)) < 6:
            c1_path.append(initial_distance_matrix[i][-2])
        elif (i not in random_init_path) and ((6 <= i < 2*len(c1_path)) or (len(c2_path) < 6)):
            c2_path.append(initial_distance_matrix[i][-2])
        elif (2*len(c1_path) <= i < length) and (i not in random_init_path):
            c3_path.append(initial_distance_matrix[i][-2])
        i += 1


def fill_matrix_path():
    initial_path()
    matrix_path.append(c1_path)
    matrix_path.append(c2_path)
    matrix_path.append(c3_path)
    print(matrix_path)


fill_matrix_path()
