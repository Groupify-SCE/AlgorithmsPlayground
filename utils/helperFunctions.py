import random
import csv
import json
import time
from Genetic.PreferencesGenetic import calculate_diversity, genetic_algorithm_with_preferences
from utils.student import Student
from typing import List
from tabulate import tabulate

def generate_random_student_list(amount: int, criteria: List[dict]) -> List[Student]:
    """
    יוצר רשימה של אובייקטי סטודנטים עם נתונים רנדומליים.

    :param amount: כמות הסטודנטים ליצירה (int).
    :param criteria: רשימת קריטריונים להגדרת הסטודנטים (List[dict]).
    :return: רשימת אובייקטי סטודנטים (List[Student]).
    
    דוגמא לקריאה: generate_random_student_list(10, [{"name": "GPA", "type": "0-100"}]) יחזיר רשימה של עשרה תלמידים עם ממוצע ציונים בין 0 ל100 ועם העדפות עם מי להיות
    """
    return [
        Student({
            "id": i, 
            "name": f"Student_{i}", 
            "preferences": generate_random_preferences(1, amount, i), 
            "criteria": generate_criteria_list(criteria)
        }) 
        for i in range(1, amount + 1)
    ]

def generate_random_preferences(min_val: int, max_val: int, exclude: int) -> List[int]:
    """
    יוצר רשימת העדפות רנדומלית לסטודנט, תוך כדי מניעת הכללת ערך מסוים.
    """
    valid_values = [num for num in range(min_val, max_val + 1) if num != exclude]
    return random.sample(valid_values, 4 if len(valid_values) >= 4 else len(valid_values))

def generate_criteria_list(criteria_definitions: List[dict]) -> List[dict]:
    """
    יוצר רשימת קריטריונים עם ערכים רנדומליים.
    """
    def generate_value(criteria_type: str) -> float:
        """
        מייצר ערך רנדומלי בהתבסס על סוג הקריטריון.
        """
        types = {
            "0-100": (0.0, 100.0),
            "0-1": (0.0, 1.0),
            "0-10": (0.0, 10.0)
        }
        if criteria_type not in types:
            raise ValueError(f"Unknown criteria type: {criteria_type}")
        
        min_val, max_val = types[criteria_type]
        return round(random.uniform(min_val, max_val), 2)
    
    criteria_list = []
    for criteria in criteria_definitions:
        name = criteria["name"]
        criteria_type = criteria["type"]
        value = generate_value(criteria_type)
        criteria_list.append({"name": name, "type": criteria_type, "value": value})
    
    return criteria_list

def print_students_table(students: List[Student]):
    """
    מדפיס טבלה של התלמידים
    """
    table_data = [
        [student.id, ', '.join(map(str, student.preferences)), f"{student.get_score():.2f}"]
        for student in students
    ]
    headers = ["ID", "Preferences", "Score"]
    print(tabulate(table_data, headers, tablefmt="grid"))

def generate_students_json(file_name: str = None, num_students: int = 10, num_criteria: int = random.randint(1, 5)) -> None:
    """
    מגריל קובץ גייסון עם פרטי תלמידים
    """
    if not file_name:
        file_name = f"students({num_students})_criteria({num_criteria})"
    students = []

    criteria_template = [
        {
            "name": f"Criteria_{i + 1}",
            "type": random.choice(["0-1", "0-10", "0-100"])
        }
        for i in range(num_criteria)
    ]

    for student_id in range(1, num_students + 1):
        # מגריל העדפות רנדומליות
        preferences = generate_random_preferences(1, num_students, student_id)

        # מגדיל קריטריונים רנדומלים
        criteria = generate_criteria_list(criteria_template)

        # יוצר את הגייסון של התלמיד
        student_data = {
            "id": student_id,
            "name": f"Student_{student_id}",
            "preferences": preferences,
            "criteria": criteria
        }
        students.append(student_data)

    # שמירה לקובץ גייסון
    with open(f"samples/{file_name}.json", "w") as file:
        json.dump(students, file, indent=4)

    print(f"Generated {num_students} students and saved to {file_name}")

def translate_file_to_students(file_name: str) -> List[Student]:
    """
    קורא קובץ גייסון ומחזיר את הרשימה של התלמידים בתור אובייקט
    """
    try:
        with open(file_name, "r") as file:
            students_data = json.load(file)
        
        students = [Student(data) for data in students_data]
        return students
    except FileNotFoundError:
        print(f"שגיאה: לא נמצא קובץ עם השם: '{file_name}'")
        return []
    except json.JSONDecodeError:
        print(f"שגיאה: נכשל בתרגום הקובץ: '{file_name}'.")
        return []
    except Exception as e:
        print(f"קרתה שגיאה לא יודעה: {e}")
        return []
    
def run_generations_experiment(students: List[Student], num_groups: int, population_size: int, mutation_rate: float, output_file: str):
    generations_to_test = range(10, 501, 10)
    results = []

    for generations in generations_to_test:
        print(f"Running {generations} generations...")
        fitness_scores = []
        for run in range(1, 11):
            best_solution = genetic_algorithm_with_preferences(students, num_groups, population_size, generations, mutation_rate)
            best_fitness = calculate_diversity(best_solution)
            fitness_scores.append(best_fitness)

        results.append([generations] + fitness_scores)

    with open(f"experiments/{output_file}.csv", mode='w', newline='') as file:
        fieldnames = ["Generations"] + [f"Run_{i}" for i in range(1, 11)]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(results)

    print(f"Experiment completed! Results saved to {output_file}")

def run_timing_experiment(students: List[Student], num_groups: int, population_size: int, mutation_rate: float, output_file: str):
    generations_to_test = range(10, 501, 10)
    results = []

    for generations in generations_to_test:
        print(f"Running {generations} generations...")
        timing_scores = []
        for run in range(1, 11):
            start_time = time.time()
            genetic_algorithm_with_preferences(students, num_groups, population_size, generations, mutation_rate)
            elapsed_time = time.time() - start_time
            timing_scores.append(elapsed_time)

        results.append([generations] + timing_scores)

    with open(f"experiments/{output_file}.csv", mode='w', newline='') as file:
        fieldnames = ["Generations"] + [f"Run_{i}" for i in range(1, 11)]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(results)

    print(f"Timing experiment completed! Results saved to {output_file}")

def run_population_experiment(students: List[Student], num_groups: int, generations_size: int, mutation_rate: float, output_file: str):
    population_to_test = [5] + list(range(10, 501, 10))
    results = []

    for population in population_to_test:
        print(f"Running {population} population...")
        fitness_scores = []
        for run in range(1, 11):
            best_solution = genetic_algorithm_with_preferences(students, num_groups, population, generations_size, mutation_rate)
            best_fitness = calculate_diversity(best_solution)
            fitness_scores.append(best_fitness)

        results.append([population] + fitness_scores)

    with open(f"experiments/{output_file}.csv", mode='w', newline='') as file:
        fieldnames = ["Populations"] + [f"Run_{i}" for i in range(1, 11)]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(results)

    print(f"Experiment completed! Results saved to {output_file}")

def run_population_timing_experiment(students: List[Student], num_groups: int, generations_size: int, mutation_rate: float, output_file: str):
    population_to_test = [5] + list(range(10, 501, 10))
    results = []

    for population in population_to_test:
        print(f"Running {population} population...")
        timing_scores = []
        for run in range(1, 11):
            start_time = time.time()
            genetic_algorithm_with_preferences(students, num_groups, population, generations_size, mutation_rate)
            elapsed_time = time.time() - start_time
            timing_scores.append(elapsed_time)

        results.append([population] + timing_scores)

    with open(f"experiments/{output_file}.csv", mode='w', newline='') as file:
        fieldnames = ["Populations"] + [f"Run_{i}" for i in range(1, 11)]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(results)

    print(f"Experiment completed! Results saved to {output_file}")

def run_mutation_experiment(students: List[Student], num_groups: int, generations_size: int, population_size: int, output_file: str):
    mutation_rate_to_test = list(range(5, 101, 5))
    results = []

    for mutation_rate in mutation_rate_to_test:
        print(f"Running {mutation_rate}% population...")
        fitness_scores = []
        for run in range(1, 11):
            best_solution = genetic_algorithm_with_preferences(students, num_groups, population_size, generations_size, mutation_rate/100)
            best_fitness = calculate_diversity(best_solution)
            fitness_scores.append(best_fitness)
        results.append([f"{mutation_rate}%"] + fitness_scores)

    with open(f"experiments/{output_file}.csv", mode='w', newline='') as file:
        fieldnames = ["Mutation Rate"] + [f"Run_{i}" for i in range(1, 11)]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(results)

    print(f"Experiment completed! Results saved to {output_file}")

def run_mutation_timing_experiment(students: List[Student], num_groups: int, generations_size: int, population_size: int, output_file: str):
    mutation_rate_to_test = list(range(5, 101, 5))
    results = []

    for mutation_rate in mutation_rate_to_test:
        print(f"Running {mutation_rate}% population...")
        timing_scores = []
        for run in range(1, 11):
            start_time = time.time()
            genetic_algorithm_with_preferences(students, num_groups, population_size, generations_size, mutation_rate/100)
            elapsed_time = time.time() - start_time
            timing_scores.append(elapsed_time)
        results.append([f"{mutation_rate}%"] + timing_scores)

    with open(f"experiments/{output_file}.csv", mode='w', newline='') as file:
        fieldnames = ["Mutation Rate"] + [f"Run_{i}" for i in range(1, 11)]
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(results)

    print(f"Experiment completed! Results saved to {output_file}")