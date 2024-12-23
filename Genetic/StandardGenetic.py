import random
import statistics
import heapq
from typing import List, Tuple
from utils.student import Student

def initialize_groups(students: List[Student], num_groups: int) -> List[List[Student]]:
    """
    יוצר קבוצות התחלתיות
    """
    random.shuffle(students)
    groups = [[] for _ in range(num_groups)]
    for i, student in enumerate(students):
        groups[i % num_groups].append(student)
    return groups

def calculate_diversity(groups: List[List[Student]]) -> float:
    """
    פונקציית חישוב הגיוון של תוצאה
    """
    group_diversities = []

    for group in groups:
        scores = [student.get_score() for student in group]
        if len(scores) > 1:  # סטיית תקן מוגדרת רק עבור יותר מנתון אחד
            diversity = statistics.stdev(scores)
        else:
            diversity = 0  # אין גיוון בקבוצה עם תלמיד אחד
        group_diversities.append(diversity)

    # ממוצע הגיוון בקבוצות
    mean_diversity = sum(group_diversities) / len(group_diversities)

    # שונות בין הגיוונים בקבוצות (עונש על חוסר אחידות)
    diversity_variance = statistics.stdev(group_diversities) if len(group_diversities) > 1 else 0

    # ניקוד כולל: ממוצע הגיוון - שונות בין הקבוצות (אנחנו רוצים שונות נמוכה)
    total_score = mean_diversity - diversity_variance
    return total_score

def generate_initial_population(students: List[Student], num_groups: int, population_size: int) -> List[List[List[Student]]]:
    """
    יוצרת אוכלוסייה ראשונית של פתרונות.
    כל פתרון הוא חלוקה של התלמידים לקבוצות.
    """
    population = []  # רשימת פתרונות
    for _ in range(population_size):
        groups = initialize_groups(students, num_groups)  # חלוקה אקראית
        population.append(groups)
    return population

def calculate_population_fitness(population: List[List[List[Student]]]) -> List[float]:
    """
    מחשבת את הכושר עבור כל פתרון באוכלוסייה.
    """
    fitness_scores = []
    for groups in population:
        fitness = calculate_diversity(groups)  # חישוב הגיוון
        fitness_scores.append(fitness)
    return fitness_scores

def selection(population: List[List[List[Student]]], fitness_scores: List[float]) -> Tuple[Student, Student]:
    """
    מחזיר את שני ההורים עם הניקוד הגבוה ביותר
    """
    if len(fitness_scores) >= 2:
        largest_scores = heapq.nlargest(2, fitness_scores)
    elif len(fitness_scores) == 1:
        return population[0]
    else:
        return None
        
    parent1_index = population[fitness_scores.index(largest_scores[0])]
    parent2_index = population[fitness_scores.index(largest_scores[1])]
    return parent1_index, parent2_index

def crossover(parent1: List[List[Student]], parent2: List[List[Student]]) -> List[List[Student]]:
    """
    מבצע הכלאה בין שני הורים ליצירת ילד חדש, תוך הבטחת חלוקה מלאה של כל התלמידים.
    """
    all_students = {student.id: student for group in parent1 + parent2 for student in group}

    # חלוקה ראשונית מהורה 1
    child = [group[:] for group in parent1]

    # שמירה על התלמידים שכבר הוקצו
    assigned_students = {student.id for group in child for student in group}

    # הוספת תלמידים חסרים מהורה 2
    for group in parent2:
        for student in group:
            if student.id not in assigned_students:
                smallest_group = min(child, key=len)
                smallest_group.append(student)
                assigned_students.add(student.id)

    # בדיקה אם כל התלמידים מוקצים
    remaining_students = list(all_students.keys() - assigned_students)
    for student_id in remaining_students:
        smallest_group = min(child, key=len)
        smallest_group.append(all_students[student_id])

    return child

def mutate(groups: List[List[Student]], mutation_rate: float) -> List[List[Student]]:
    """
    מבצע מוטציה על פתרון עם סיכוי מסוים, תוך הבטחת חלוקה מלאה של כל התלמידים.
    """
    if random.random() < mutation_rate:
        group1, group2 = random.sample(range(len(groups)), 2)
        if groups[group1] and groups[group2]:
            # בחירת תלמידים להחלפה
            student1 = random.choice(groups[group1])
            student2 = random.choice(groups[group2])

            # החלפה
            groups[group1].remove(student1)
            groups[group2].remove(student2)
            groups[group1].append(student2)
            groups[group2].append(student1)
    return groups

def update_population(population: List[List[List[Student]]], fitness_scores: List[float], child: List[List[Student]]) -> None:
    """
    מעדכן את האוכלוסייה על ידי החלפת הפתרון הגרוע ביותר בילד החדש (אם הילד טוב יותר).
    """
    # חישוב הכושר של הילד
    child_fitness = calculate_diversity(child)

    # מציאת הפתרון הגרוע ביותר
    worst_index = fitness_scores.index(min(fitness_scores))

    # החלפת הפתרון הגרוע בילד אם הוא טוב יותר
    if child_fitness > fitness_scores[worst_index]:
        population[worst_index] = child
        fitness_scores[worst_index] = child_fitness

def genetic_algorithm(students: List[Student], num_groups: int, population_size: int, generations: int, mutation_rate: float):
    # יצירת אוכלוסייה ראשונית
    population = generate_initial_population(students, num_groups, population_size)
    fitness_scores = calculate_population_fitness(population)

    for generation in range(generations):
        # בחירת הורים
        parent1, parent2 = selection(population, fitness_scores)

        # יצירת ילד חדש
        child = crossover(parent1, parent2)
        mutated_child = mutate(child, mutation_rate)

        # עדכון האוכלוסייה
        update_population(population, fitness_scores, mutated_child)

        # הדפסת מידע על הדור
        best_fitness = max(fitness_scores)
        print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

    # מחזירים את הפתרון הטוב ביותר
    best_index = fitness_scores.index(max(fitness_scores))
    return population[best_index]
