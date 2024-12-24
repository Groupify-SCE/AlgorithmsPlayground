from utils.helperFunctions import generate_random_student_list, generate_students_json, print_students_table
from Genetic.StandardGenetic import genetic_algorithm
from Genetic.PreferencesGenetic import genetic_algorithm_with_preferences

AMOUNT_OF_STUDENTS = 15
CRITERIA_LIST = [{"name": "GPA", "type": "0-100"}]

def test_standard_genetic():
    # פרמטרים
    num_groups = 3
    population_size = 5
    generations = 50
    mutation_rate = 0.3

    # הרצה
    best_solution = genetic_algorithm(students, num_groups, population_size, generations, mutation_rate)

    # הדפסת הפתרון הטוב ביותר
    print("\nBest Solution:")
    for i, group in enumerate(best_solution, 1):
        print(f"Group {i}: {group}")

def test_preferences_genetic():
    # פרמטרים
    num_groups = 3
    population_size = 5
    generations = 50
    mutation_rate = 0.3

    # הרצה
    best_solution = genetic_algorithm_with_preferences(students, num_groups, population_size, generations, mutation_rate)

    # הדפסת הפתרון הטוב ביותר
    print("\nBest Solution:")
    for i, group in enumerate(best_solution, 1):
        print(f"Group {i} ({len(group)}): {group}")

if __name__ == "__main__":
    students = generate_random_student_list(AMOUNT_OF_STUDENTS, CRITERIA_LIST)
    print_students_table(students)
    generate_students_json(num_students=10, num_criteria=2)
