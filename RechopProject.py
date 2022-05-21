import copy
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


def bellmankalaba_optimizer(index_list, current_best, fixed_index, matrix, optimized_list):
    for i in range(1, len(index_list)):
        max1, min1 = max(index_list[i], fixed_index), min(index_list[i], fixed_index)
        max2, min2 = max(current_best, fixed_index), min(current_best, fixed_index)
        if matrix[max1][min1] < matrix[max2][min2]:
            current_best = index_list[i]
    optimized_list.append(current_best)
    index_list.remove(current_best)


def optimize_path_list(index_list, matrix):
    optimized_list = [index_list[0]]
    index_list.remove(index_list[0])
    index_list.remove(index_list[-1])
    fixed_index, current_best = optimized_list[-1], index_list[0]
    while len(index_list) > 1:
        bellmankalaba_optimizer(index_list, current_best, fixed_index, matrix, optimized_list)
        fixed_index = optimized_list[-1]
        current_best = index_list[0]
    optimized_list.append(index_list[0])
    optimized_list.append(0)
    return optimized_list


def optimize_index_matrix(index_matrix, distance_matrix):
    optimized_matrix = []
    for i in index_matrix:
        optimized_matrix.append(optimize_path_list(i, distance_matrix))
    return optimized_matrix


def c_index_init(current_matrix_index):
    """Initialisation des indices de commune à traverser par les trois camions"""
    index_path_list = list(range(1, 20))
    len_list1, len_list2, len_list3 = 7, 7, 8
    generate_index_path(current_matrix_index[0], len_list1, index_path_list)
    generate_index_path(current_matrix_index[1], len_list2, index_path_list)
    generate_index_path(current_matrix_index[2], len_list3, index_path_list)

    return current_matrix_index

def get_verified_matrix(current_index_matrix):
    new_matrix = c_index_init(current_index_matrix)
    check = check_amount(amount_list, new_matrix)
    while not check:
        t_matrix = [[],[],[]]
        current_matrix = c_index_init(t_matrix)
        check = check_amount(amount_list,current_matrix)
        if check == True:
            return current_matrix
    return new_matrix


def calculate_distance_risk(distance_list, risk_list):
    total_distance = 0
    total_risk = 0
    for i in range(3):
        total_distance += distance_list[i]
        total_risk += risk_list[i]

    return total_distance, total_risk


def find_path_dist_risk(all_index_list, current_matrix_path):
    """calcul de la distance totale des camions et le risque correspondant
    avec Generation d'une matrice de distances entre les communes traversees par les trois camions
    """
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
    distance, risk = calculate_distance_risk(dist_foreach_path, risk_foreach_path)
    return distance, risk


def compare_solution(distance1, risk1, distance2, risk2):
    """Cette fonction compare deux solutions et renvoie True si la solution
    précédente est plus optimale, False si non"""
    more_optimal = True
    best_distance, best_risk = distance1, risk1

    if distance2 < distance1 and risk2 < risk1:
        best_distance, best_risk = distance2, risk2
        more_optimal = False

    print(best_distance, best_risk)

    return more_optimal


def get_new_solution(matrix_index, matrix_path):
    optimized_matrix = get_verified_matrix(matrix_index)
    distance, risk = find_path_dist_risk(optimized_matrix, matrix_path)
    return [optimized_matrix, distance, risk]


def find_optimal_sol():
    """Cette fonction génère plusieurs solutions, dont les chemins (random)
        sont optimisées par l'algorithme de Bellman Kallaba"""
    mat_index, mat_path,  = [[], [], []], [[], [], []]
    current_sol = get_new_solution(mat_index, mat_path)
    for i in range(2000):
        new_mat_path, new_matrix_index = [[], [], []], [[], [], []]
        new_sol = get_new_solution(new_matrix_index, new_mat_path)
        print(new_sol)
        current_optimal = compare_solution(current_sol[1], current_sol[2], new_sol[1], new_sol[2])
        if not current_optimal:
            current_sol = copy.deepcopy(new_sol)
            print('The current optimal solution is : ', current_sol[0])

def amount_computing(amount_list,matrix_path):
    list_of_amount = []
    for truck in matrix_path:
        amount = 0
        for i in range(1,len(truck)-1):
            amount += amount_list[truck[i]-1]
        list_of_amount.append(amount)
    return list_of_amount

def check_amount(amount_list, matrix_path):
    total_amount = 851949.0000000001
    res = True
    list_of_amount = amount_computing(amount_list,matrix_path)
    for amount in list_of_amount:
        if amount>= 0.5*total_amount:
            res = False
    return res

find_optimal_sol()
