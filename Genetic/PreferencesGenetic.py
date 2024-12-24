import random
import statistics
import heapq
from typing import List, Tuple
from utils.student import Student

def initialize_groups(students: List[Student], num_groups: int) -> List[List[Student]]:
    """
    הערה מקורית: יוצר קבוצות התחלתיות
    מה הוספנו? לא ביצענו באופן אקראי לחלוטין, אנחנו מתאימים תלמידים לפי התאמות אישיות
    """
    # ניצור את הקבוצות ריקות
    groups = [[] for _ in range(num_groups)]
    # נשמור תלמידים שהכנסנו לקבוצה
    assigned_students = set()

    # נחשב את הגודל המקסימלי של כל קבוצה
    max_group_size = len(students) // num_groups + (1 if len(students) % num_groups != 0 else 0)
    
    random.shuffle(students)
    # נרוץ על כל תלמיד, ננסה להכניס אותו לקבוצה רק אם יש לו את אחת מהעדפות שלו בקבוצה
    # ואם הקבוצה לא עברה את הגודל המקסימלי
    for student in students:
        for group in groups:
            if len(group) < max_group_size and any(preference in [s.id for s in group] for preference in student.preferences):
                group.append(student)
                assigned_students.add(student.id)
                break

        # אם התלמיד לא הוכנס לאף קבוצה, נכניס אותו לקבוצה הכי קטנה (אם היא לא מלאה)
        if student.id not in assigned_students:
            smallest_group = min(groups, key=len)
            if len(smallest_group) < max_group_size:
                smallest_group.append(student)
                assigned_students.add(student.id)

    # נרוץ על התלמידים שעוד לא הוכנסו לקבוצות, כל אחד מהם בתורו נכניס לקבוצה הקטנה ביותר (אם היא לא מלאה)
    remaining_students = [student for student in students if student.id not in assigned_students]
    for student in remaining_students:
        for group in groups:
            if len(group) < max_group_size:
                group.append(student)
                break

    return groups

def calculate_diversity(groups: List[List[Student]]) -> float:
    """
    הערה מקורית: פונקציית חישוב הגיוון של תוצאה
    מה הוספנו? על כל תלמיד שבקבוצה עם לפחות אחת מהעדפות שלו הוספנו נקודה לתוצאה
    """
    group_diversities = []
    preference_score = 0

    for group in groups:
        scores = [student.get_score() for student in group]
        if len(scores) > 1:  # סטיית תקן מוגדרת רק עבור יותר מנתון אחד
            diversity = statistics.stdev(scores)
        else:
            diversity = 0  # אין גיוון בקבוצה עם תלמיד אחד
        group_diversities.append(diversity)

        # נרוץ על כל התלמידים בקבוצה, נבדוק אם הוא עם לפחות העדפה אחת שלו. אם כן, נוסיף נקודה לציון
        for student in group:
            if any(preference in [s.id for s in group] for preference in student.preferences):
                preference_score += 1

    # ממוצע הגיוון בקבוצות
    mean_diversity = sum(group_diversities) / len(group_diversities)

    # שונות בין הגיוונים בקבוצות (עונש על חוסר אחידות)
    diversity_variance = statistics.stdev(group_diversities) if len(group_diversities) > 1 else 0

    # ניקוד כולל: ממוצע הגיוון - שונות בין הקבוצות ונוסיף את ניקוד על ההתאמה האישית (אנחנו רוצים שונות נמוכה)
    total_score = mean_diversity + preference_score - diversity_variance
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
        
    parent1 = population[fitness_scores.index(largest_scores[0])]
    parent2 = population[fitness_scores.index(largest_scores[1])]
    return parent1, parent2

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

def genetic_algorithm_with_preferences(students: List[Student], num_groups: int, population_size: int, generations: int, mutation_rate: float):
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
