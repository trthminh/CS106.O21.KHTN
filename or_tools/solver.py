from ortools.algorithms.python import knapsack_solver
import time
import os
from tqdm import tqdm
def process(capacities, values, weights, result_path_file):
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )
    weights = [weights]

    solver.init(values, weights, capacities)
    solver.set_time_limit(3 * 60)
    start = time.time()
    computed_value = solver.solve()
    end = time.time()

    packed_items = []
    packed_weights = []
    total_weight = 0
    f = open(result_path_file, "w+")
    # f.write("Time run: "+str(end-start) + '\n')
    # print("Total value =", computed_value)
    f.write("Total value: " + str(computed_value) + '\n')
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    # print("Time run:", end-start)
    f.write("Total weight: "+str(total_weight) +'\n')
    # print("Total weight:", total_weight)
    # f.write("Packed items: "+ str(packed_items) + '\n')
    # print("Packed items:", packed_items)
    # f.write("Packed_weights: "+str(packed_weights) +'\n')
    # print("Packed_weights:", packed_weights)
    # print("Write file successfull")
    packed_items_best = [x for x in range(0, len(weights[0]))
                    if solver.best_solution_contains(x)]
    if (solver.is_solution_optimal()):
        # print("Optimal answer")
        f.write("True\n")
    else:
        # print("Non-optimal answer")
        f.write("False\n")
    f.close()
    
def read_file(path_file):
    f = open(path_file, 'r')
    n = None
    c = None
    values = []
    weights = []
    while True:
        txt = f.readline()
        if txt == "":
            break
        else:
            if txt == '\n':
                continue
            else:
                if n == None:
                    n = int(txt)
                elif c == None:
                    c = int(txt)
                else:
                    p, w = map(int, txt.split())
                    values.append(p)
                    weights.append(w)
    f.close()
    capacities = [c]
    return n, capacities, values, weights

if __name__ == "__main__":
    root_path = './kplib'
    path_result = './results'
    for folder_name in tqdm(os.listdir(root_path)):
        if folder_name[0] != '.' and folder_name[0] != 'R':
            path_folder = os.path.join(root_path, folder_name)
            tmp = folder_name
            for sub_folder1 in os.listdir(path_folder):
                path_sub_folder1 = os.path.join(path_folder, sub_folder1)
                tmp_1 = tmp + '_' + sub_folder1
                isVisited = False
                for sub_folder2 in os.listdir(path_sub_folder1):
                    path_sub_folder2 = os.path.join(path_sub_folder1, sub_folder2)
                    tmp_2 = tmp_1 + '_' + sub_folder2
                    if isVisited:
                        break
                    for fi in os.listdir(path_sub_folder2):
                        path_file = os.path.join(path_sub_folder2, fi)
                        result_path_file = tmp_2 + '_' + fi
                        result_path_file = os.path.join(path_result, result_path_file)
                        n, capacities, values, weights = read_file(path_file)
                        process(capacities, values, weights, result_path_file)
                        isVisited = True
                        if isVisited == True:
                            break
                    

