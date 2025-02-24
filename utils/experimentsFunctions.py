import random
import csv
import json
import time
from Genetic.PreferencesGenetic import calculate_diversity, genetic_algorithm_with_preferences
from ABC.PrefrencesABC import abc_algorithm_with_prefrences
from utils.helperFunctions import parse_problem_files
from utils.student import Student
from typing import Dict, List, Tuple
from tabulate import tabulate

def run_experiments():
    input_sizes = [60, 120, 240, 480, 960]
    students: Dict[str, List[List[Student]]] = {}
    num_groups: Dict[str, List[int]] = {}
    for input in input_sizes:
        students[str(input)] = []
        num_groups[str(input)] = []
        for i in range(1, 11):
            res_students, res_groups = parse_problem_files(f"diversity/RanInt_n{input}_ss_{i:02d}.txt", f"acceptance/acceptance{input}_{i:02d}.txt")
            students[str(input)].append(res_students)
            num_groups[str(input)].append(res_groups)
    for input_size in input_sizes[2:]:
        #experiment_ABC_iterations(students[str(input_size)], num_groups[str(input_size)], 10)
        experiment_Genetic_generations(students[str(input_size)], num_groups[str(input_size)], 0.3)

def experiment_ABC_iterations(students: List[List[Student]], num_groups: List[int], limit: int):
    output_file = f"ABC/Iterations_{len(students[0])}"
    # ציר X
    iterations = [1] + list(range(5, 501, 5))
    # ציר Y
    results_fitness = []
    results_time = []

    for iteration in iterations:
        print(f"Running ABC on {iteration} iterations...")
        score_sum = 0
        time_sum = 0
        for i in range(10):
            start_time = time.time()
            result = abc_algorithm_with_prefrences(students[i], num_groups[i], iteration, limit)
            elapsed_time = time.time() - start_time
            time_sum += elapsed_time
            score = calculate_diversity(result)
            score_sum += score
        results_fitness.append((score_sum/10))
        results_time.append((time_sum/10))
    
    with open(f"experiments/{output_file}_Fitness.csv", mode="w", newline='') as file:
        fieldnames = ["Iteration", "AVG Score"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(iterations, results_fitness))

    print(f"Experiment completed! Results saved to {output_file}_Fitness.csv")

    with open(f"experiments/{output_file}_Time.csv", mode="w", newline='') as file:
        fieldnames = ["Iteration", "AVG Time"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(iterations, results_time))

    print(f"Experiment completed! Results saved to {output_file}_Time.csv")

def experiment_ABC_limit(students: List[List[Student]], num_groups: List[int], iterations: int):
    output_file = f"ABC/Limit_{len(students[0])}"
    # ציר X
    limits = list(range(1, 51))
    # ציר Y
    results_fitness = []
    results_time = []

    for limit in limits:
        print(f"Running ABC on {limit} limit...")
        score_sum = 0
        time_sum = 0
        for i in range(10):
            start_time = time.time()
            result = abc_algorithm_with_prefrences(students[i], num_groups[i], iterations, limit)
            elapsed_time = time.time() - start_time
            time_sum += elapsed_time
            score = calculate_diversity(result)
            score_sum += score
        results_fitness.append((score_sum/10))
        results_time.append((time_sum/10))
    
    with open(f"experiments/{output_file}_Fitness.csv", mode="w", newline='') as file:
        fieldnames = ["Limit", "AVG Score"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(limits, results_fitness))

    print(f"Experiment completed! Results saved to {output_file}_Fitness.csv")

    with open(f"experiments/{output_file}_Time.csv", mode="w", newline='') as file:
        fieldnames = ["Limit", "AVG Time"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(limits, results_time))

    print(f"Experiment completed! Results saved to {output_file}_Time.csv")

def experiment_Genetic_generations(students: List[List[Student]], num_groups: List[int], mutation: float):
    output_file = f"Genetic/Generations_{len(students[0])}"
    # ציר X
    generations = [1] + list(range(5, 501, 5))
    # ציר Y
    results_fitness = []
    results_time = []

    for generation in generations:
        print(f"Running Genetic on {generation} generations...")
        score_sum = 0
        time_sum = 0
        for i in range(10):
            start_time = time.time()
            result = genetic_algorithm_with_preferences(students[i], num_groups[i], generation, mutation)
            elapsed_time = time.time() - start_time
            time_sum += elapsed_time
            score = calculate_diversity(result)
            score_sum += score
        results_fitness.append((score_sum/10))
        results_time.append((time_sum/10))
    
    with open(f"experiments/{output_file}_Fitness.csv", mode="w", newline='') as file:
        fieldnames = ["Generation", "AVG Score"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(generations, results_fitness))

    print(f"Experiment completed! Results saved to {output_file}_Fitness.csv")

    with open(f"experiments/{output_file}_Time.csv", mode="w", newline='') as file:
        fieldnames = ["Generation", "AVG Time"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(generations, results_time))

    print(f"Experiment completed! Results saved to {output_file}_Time.csv")

def experiment_Genetic_mutation(students: List[List[Student]], num_groups: List[int], generations: int):
    output_file = f"Genetic/Mutation_{len(students[0])}"
    # ציר X
    mutations = [float(x/100) for x in list(range(1, 101, 1))]
    # ציר Y
    results_fitness = []
    results_time = []

    for mutation in mutations:
        print(f"Running Genetic on {mutation} mutation...")
        score_sum = 0
        time_sum = 0
        for i in range(10):
            start_time = time.time()
            result = genetic_algorithm_with_preferences(students[i], num_groups[i], generations, mutation)
            elapsed_time = time.time() - start_time
            time_sum += elapsed_time
            score = calculate_diversity(result)
            score_sum += score
        results_fitness.append((score_sum/10))
        results_time.append((time_sum/10))
    
    with open(f"experiments/{output_file}_Fitness.csv", mode="w", newline='') as file:
        fieldnames = ["Mutation", "AVG Score"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(mutations, results_fitness))

    print(f"Experiment completed! Results saved to {output_file}_Fitness.csv")

    with open(f"experiments/{output_file}_Time.csv", mode="w", newline='') as file:
        fieldnames = ["Mutation", "AVG Time"]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(zip(mutations, results_time))

    print(f"Experiment completed! Results saved to {output_file}_Time.csv")