from utils.helperFunctions import generate_random_student_list, generate_students_json, print_students_table, run_generations_experiment, run_mutation_experiment, run_mutation_timing_experiment, run_population_experiment, run_population_timing_experiment, run_timing_experiment, translate_file_to_students, parse_problem_files
from Genetic.StandardGenetic import genetic_algorithm
from Genetic.PreferencesGenetic import genetic_algorithm_with_preferences
from ABC.StandardABC import abc_algorithm
from ABC.PrefrencesABC import abc_algorithm_with_prefrences
from termcolor import colored


def get_filename(num_students: int, num_criteria: int):
    return f"samples\students({num_students})_criteria({num_criteria}).json"

def test_standard_genetic(students, num_groups):
    # פרמטרים
    population_size = 5
    generations = 50
    mutation_rate = 0.3

    # הרצה
    best_solution = genetic_algorithm(students, num_groups, population_size, generations, mutation_rate)

    # הדפסת הפתרון הטוב ביותר
    print_solution_with_highlights(best_solution)

def test_preferences_genetic(students, num_groups):
    # פרמטרים
    population_size = 5
    generations = 50
    mutation_rate = 0.3

    # הרצה
    best_solution = genetic_algorithm_with_preferences(students, num_groups, population_size, generations, mutation_rate)

    # הדפסת הפתרון הטוב ביותר
    print_solution_with_highlights(best_solution)

def test_standard_abc(students, num_groups):
    # פרמטרים
    num_iterations = 50
    limit = 10
    # הרצה
    best_solution = abc_algorithm(students, num_groups, num_iterations, limit)

    # הדפסת הפתרון הטוב ביותר
    print_solution_with_highlights(best_solution)

def test_prefrences_abc(students, num_groups):
    # פרמטרים
    num_iterations = 50
    limit = 10
    # הרצה
    best_solution = abc_algorithm_with_prefrences(students, num_groups, num_iterations, limit)

    # הדפסת הפתרון הטוב ביותר
    print_solution_with_highlights(best_solution)

def print_solution_with_highlights(solution):
    """
    מדפיסה את הפתרון בצורה מוארת: ירוק אם התלמיד בקבוצה עם מישהו שהוא רוצה להיות איתו, אדום אם לא.
    """
    print("\nBest Solution:")
    for i, group in enumerate(solution, 1):
        print(f"Group {i} ({len(group)}):")
        group_ids = [student.id for student in group]
        for student in group:
            in_group_with_preferences = any(pref in group_ids for pref in student.preferences)
            if in_group_with_preferences:
                print(colored(f"  {student.id}: {student.preferences}", "green"))
            else:
                print(colored(f"  {student.id}: {student.preferences}", "red"))


if __name__ == "__main__":
    ranint_path = "RanInt_n060_ss_01.txt"
    acceptance_path = "acceptance60_1.txt"
    students, num_groups = parse_problem_files(ranint_path, acceptance_path)
    test_prefrences_abc(students, num_groups)
