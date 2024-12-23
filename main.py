from utils.helperFunctions import generate_random_student_list, print_students_table
from Genetic.StandardGenetic import genetic_algorithm

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

if __name__ == "__main__":
    students = generate_random_student_list(AMOUNT_OF_STUDENTS, CRITERIA_LIST)
    print_students_table(students)
