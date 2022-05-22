import copy
import random
from matplotlib import pyplot as plt

"print(initial_distance_matrix)"

amount_list = [84975.8, 24455.9, 17701.6, 131380.2,
               33756.1, 30436.7, 39389.7, 17641.4, 60841.9,
               36822.8, 15397.9, 67971.4, 33948.6, 18766.3,
               91189, 59252.9, 17633, 40913.6, 29474.2]
max_people_cities = [1, 4, 15]


def generate_index_path(c_path_index_list, max_index_city, len_list, index_path_list):
    """Generation des indices de commune à traverser par un camion c"""
    c_path_index_list.append(0)
    c_path_index_list.append(max_people_cities[max_index_city])
    while len(index_path_list) != 0 and len(c_path_index_list) != len_list:
        index = random.randint(0, len(index_path_list) - 1)
        c_path_index_list.append(index_path_list[index])
        index_path_list.remove(index_path_list[index])
    c_path_index_list.append(0)


def bellmankalaba_optimizer(index_list, current_best, fixed_index, matrix, optimized_list):
    """cherche la plus petite distance à parcourir pour aller vers une autre commune"""
    for i in range(1, len(index_list)):
        max1, min1 = max(index_list[i], fixed_index), min(index_list[i], fixed_index)
        max2, min2 = max(current_best, fixed_index), min(current_best, fixed_index)
        if matrix[max1][min1] < matrix[max2][min2]:
            current_best = index_list[i]
    optimized_list.append(current_best)
    index_list.remove(current_best)


def optimize_path_list(index_list, matrix):
    """Optimise le chemin d'un camion en permuttant les communes
    par lesquelles qu'il parcourt """
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


def optimize_index_matrix(index_matrix, init_matrix):
    """Optimise et renvoie une matrice grâce à l'algo
    de Bellman Kalaba"""
    optimized_matrix = []
    index_matrix_copy = copy.deepcopy(index_matrix)
    for i in index_matrix_copy:
        optimized_matrix.append(optimize_path_list(i, init_matrix))
    return optimized_matrix


def amount_computing(matrix_path):
    """Renvoie une liste de montant transportés par chaque camion"""
    list_of_amount = []
    for truck in matrix_path:
        amount = 0
        for i in range(1, len(truck) - 1):
            amount += amount_list[truck[i] - 1]
        list_of_amount.append(amount)
    return list_of_amount


def check_amount(index_matrix):
    """Renvoie True si le montant contenu dans un camion dépasse la moitié du montant total"""
    total_amount = 851949.0000000001
    res = True
    list_of_amount = amount_computing(index_matrix)
    for amount in list_of_amount:
        if amount >= 0.5 * total_amount:
            res = False
    return res


def c_index_init(current_matrix_index):
    """Initialisation des indices de commune à traverser par les trois camions"""
    index_path_list = list(range(1, 20))
    len_list1, len_list2, len_list3 = 7, 7, 8
    max_index_city = random.sample(range(3), 3)
    for i in max_index_city:
        index_path_list.remove(max_people_cities[max_index_city[i]])
    generate_index_path(current_matrix_index[0], max_index_city[0], len_list1, index_path_list)
    generate_index_path(current_matrix_index[1], max_index_city[1], len_list2, index_path_list)
    generate_index_path(current_matrix_index[2], max_index_city[2], len_list3, index_path_list)

    return current_matrix_index


def get_verified_matrix(current_index_matrix):
    """Renvoie une matrice qui vérifie la contrainte selon laquelle un camion
    ne doit pas contenir plus de 50% du montant total"""
    new_matrix = c_index_init(current_index_matrix)
    check = check_amount(new_matrix)
    while not check:
        t_matrix = [[], [], []]
        current_matrix = c_index_init(t_matrix)
        check = check_amount(current_matrix)
        if check:
            return current_matrix
    return new_matrix


def calculate_distance_risk(distance_list, risk_list):
    """Somme des distances des différentes communes"""
    total_distance = 0
    total_risk = 0
    for i in range(3):
        total_distance += distance_list[i]
        total_risk += risk_list[i]

    return total_distance, total_risk


def find_path_dist_risk(index_matrix):
    """calcul de la distance totale des camions et le risque correspondant
    avec Generation d'une matrice de distances entre les communes traversees par les trois camions
    """

    dist_foreach_path, risk_foreach_path = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]

    current_index = 0
    for i in index_matrix:
        c = 0
        while c < len(i) - 1:
            get_distance = initial_distance_matrix[max(i[c], i[c + 1])][min(i[c], i[c + 1])]
            dist_foreach_path[current_index] += get_distance
            if c != 0 and c < len(i) - 1 and i[c] < 19:
                risk_foreach_path[current_index] += get_distance * amount_list[i[c]]
            c += 1
        current_index += 1
    distance, risk = calculate_distance_risk(dist_foreach_path, risk_foreach_path)
    return distance, risk


def compare_solution(distance1, risk1, distance2, risk2):
    """Cette fonction compare deux solutions et renvoie True si la solution
    précédente est plus optimale, False si non"""

    more_optimal = True

    if (distance2 < distance1 and risk2 < risk1) or distance2 < distance1:  # or (distance2 < distance1 or risk2 < risk1)
        best_distance, best_risk = distance2, risk2
        more_optimal = False
        print(best_distance, best_risk)

    return more_optimal


def get_new_solution(matrix_index, fixed_count, counter):
    """Génère une nouvelle solution qui respecte toutes les contraintes"""
    if counter < fixed_count:
        index_matrix = get_verified_matrix(matrix_index)
    else:
        checked_matrix = get_verified_matrix(matrix_index)
        index_matrix = optimize_index_matrix(checked_matrix, initial_distance_matrix)
    distance, risk = find_path_dist_risk(index_matrix)
    return [index_matrix, distance, risk]


def find_first_population(iteration, first_population_list, fixed_count, counter):
    """Cette fonction génère plusieurs solutions dont les chemins sont pris au hazard"""
    mat_index = [[], [], []]
    current_sol = get_new_solution(mat_index, fixed_count, counter)
    print('The current optimal solution is : ', current_sol[0])
    # print(current_sol[1], current_sol[2])
    first_population_list.append(current_sol)
    while iteration > len(first_population_list):
        new_matrix_index = [[], [], []]
        new_sol = get_new_solution(new_matrix_index, fixed_count, counter)
        current_optimal = compare_solution(current_sol[1], current_sol[2], new_sol[1], new_sol[2])
        if not current_optimal:
            current_sol = copy.deepcopy(new_sol)
            first_population_list.append(current_sol)
            write_solution_to_file(current_sol)
            print('The current optimal solution is : ', current_sol[0])
    print(len(first_population_list))
    return first_population_list


def get_genes(iteration, nb_gene):
    """Permet de générer plusieurs ensembles de solutions qui convergent différemment"""
    gene_list = []
    fixed_count = 0
    counter = 1
    for i in range(nb_gene):
        print('----------------------------------creating new genes---------------------------------------', counter)
        population = []
        sol_population = find_first_population(iteration, population, fixed_count, counter)
        gene_list.append(sol_population)
        counter += 1
    return gene_list


def swap_indexes_c(index_matrix):
    """Permet de permuter les chemins de deux camions"""
    swapped_matrix = copy.deepcopy(index_matrix)
    random_list = random.sample(range(3), 2)
    random_index = random.sample(range(2, 7), 5)
    for i in random_index:
        current_index1, current_index2 = swapped_matrix[random_list[0]][i], swapped_matrix[random_list[1]][i]
        swapped_matrix[random_list[0]][i], swapped_matrix[random_list[1]][i] = current_index2, current_index1
    return swapped_matrix


def get_mutated_sol(index_matrix):
    """Permet de générer une nouvelle solution optimisée à partir d'une autre """
    checked_amount = False
    while not checked_amount:
        swapped_matrix = swap_indexes_c(index_matrix)
        checked_amount = check_amount(swapped_matrix)
        if checked_amount:
            sol1 = mutated_sol(swapped_matrix)
            sol2 = optimized_mutated_sol(swapped_matrix)
            return sol1, sol2


def optimized_mutated_sol(swapped_matrix):
    """Optimise une solution obtenue à partir d'une autre solution"""
    optimized_swapped_matrix = optimize_index_matrix(swapped_matrix, initial_distance_matrix)
    get_sol = mutated_sol(optimized_swapped_matrix)
    return get_sol


def mutated_sol(swapped_matrix):
    """Renvoie une solution obtenue à partir d'une autre """
    distance, risk = find_path_dist_risk(swapped_matrix)
    return [swapped_matrix, distance, risk]


def add_mutated_genes(iteration, nb_genes):
    """Ajoute des solutions obtenues à partir d'une mutation dans la liste de solution existante"""
    first_gene_list = get_genes(iteration, nb_genes)
    mutated_sol_list = []
    for gene_i in first_gene_list:
        for sol_i in gene_i:
            get_mutated_sol1, get_mutated_sol2 = get_mutated_sol(sol_i[0])
            optimal1 = compare_solution(get_mutated_sol1[1], get_mutated_sol1[2],
                                        sol_i[1], sol_i[2])
            optimal2_1 = compare_solution(get_mutated_sol2[1], get_mutated_sol2[2],
                                          sol_i[1], sol_i[2])
            optimal2_2 = compare_solution(get_mutated_sol2[1], get_mutated_sol2[2],
                                          get_mutated_sol1[1], get_mutated_sol1[2])
            if optimal1:
                mutated_sol_list.append(get_mutated_sol1)
                write_solution_to_file(get_mutated_sol1)
                if optimal2_1 or optimal2_2:
                    mutated_sol_list.append(get_mutated_sol2)
                    write_solution_to_file(get_mutated_sol2)
            elif optimal2_1:
                mutated_sol_list.append(get_mutated_sol2)
                write_solution_to_file(get_mutated_sol2)
    first_gene_list.append(mutated_sol_list)
    return first_gene_list


def write_solution_to_file(solution):
    output_file = open("solution3.txt", "a")
    output_file.write(str(solution) + "\n")
# [1:-1].replace(" ", "")


initial_distance_matrix = []
f = open("distances.txt")

for line in f:
    distance_string = line.strip('\n').split(",")
    distance_float = [float(i) for i in distance_string]
    initial_distance_matrix.append(distance_float)


nb_population = 5

gene = add_mutated_genes(nb_population, 1000)


# x-axis values
x = []

# Y-axis values
y = []

for sol in gene:
    for solutions in sol:
        x.append(solutions[-2])
        y.append(solutions[-1])
#print(sorted(x), sorted(y))


# Function to plot scatter
plt.scatter(x, y)

# function to show the plot
plt.show()
