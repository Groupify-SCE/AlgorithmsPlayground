from utils.helperFunctions import generate_random_student_list, generate_students_json, print_students_table, translate_file_to_students
from Genetic.StandardGenetic import genetic_algorithm
from Genetic.PreferencesGenetic import genetic_algorithm_with_preferences

def get_filename(num_students: int, num_criteria: int):
    return f"samples\students({num_students})_criteria({num_criteria}).json"

def test_standard_genetic(students):
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

def test_preferences_genetic(students):
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
    students = translate_file_to_students(get_filename(15, 1))
    print_students_table(students)
