import random
import csv
import json
import time
from Genetic.PreferencesGenetic import calculate_diversity, genetic_algorithm_with_preferences
from ABC.PrefrencesABC import abc_algorithm_with_prefrences
from utils.student import Student
from typing import List, Tuple
from tabulate import tabulate

def experiment_ABC_iterations(students: List[Student], num_groups: int, limit: int):
    output_file = "ABC/Iterations"
    # ציר X
    iterations = list(range(1, 1001))
    # ציר Y
    results_fitness = []
    results_time = []

    for iteration in iterations:
        print(f"Running ABC on {iteration} iterations...")
        score_sum = 0
        time_sum = 0
        for _ in range(10):
            start_time = time.time()
            result = abc_algorithm_with_prefrences(students, num_groups, iteration, limit)
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

    