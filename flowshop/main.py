import copy
import random


def ms_and_tt_calculator(product_matrix):
    makespan_matrix = []
    first_row = [product_matrix[0][2]]
    for i in range(3, 12):
        first_row.append(first_row[i - 3] + product_matrix[0][i])
    makespan_matrix.append(first_row)
    for i in range(1, 200):
        makespan_matrix.append([makespan_matrix[i - 1][0] + product_matrix[i][2]])
    for r in range(1, 200):
        for c in range(1, 10):
            makespan_matrix[r].append(
                max(makespan_matrix[r][c - 1], makespan_matrix[r - 1][c]) + product_matrix[r][c + 2])
    makespan = makespan_matrix[-1][-1]
    total_tardiness = 0
    for r in range(200):
        if makespan_matrix[r][-1] > product_matrix[r][1]:
            total_tardiness += (makespan_matrix[r][-1] - product_matrix[r][1]) * product_matrix[r][0]
    return makespan, total_tardiness


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def write_solution_to_file(solution):
    output_file = open("output.txt", "a")
    output_file.write(str(solution)[1:-1].replace(" ", "") + "\n")


def permutate(first_list, matrix):
    second_list = copy.deepcopy(first_list)

    random_numbers = random.sample(range(0, 200), 2)
    swapPositions(second_list, random_numbers[0], random_numbers[1])

    first_matrix = []
    for i in range(200):
        first_matrix.append(matrix[first_list[i]])

    swapped_matrix = []
    for i in range(200):
        swapped_matrix.append(matrix[second_list[i]])

    ms1, tt1 = ms_and_tt_calculator(first_matrix)
    ms2, tt2 = ms_and_tt_calculator(swapped_matrix)

    if ms2 < ms1 and tt2 < tt1:
        return second_list
    else:
        return first_list


f = open("instance.txt")
initial_product_matrix = []
for line in f:
    product_string = line.strip('\n').split(",")
    product_int = [int(i) for i in product_string]
    initial_product_matrix.append(product_int)

for j in range(30):
    index_list = list(range(0, 200))
    for i in range(2000):
        index_list = permutate(index_list, initial_product_matrix)

    write_solution_to_file(index_list)
