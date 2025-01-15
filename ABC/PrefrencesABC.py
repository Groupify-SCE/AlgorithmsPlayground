import random
import statistics
from typing import List
from utils.student import Student

GLOBAL_MAX = []
GLOBAL_MAX_VAL = float("-inf")
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
        scores = []
        if group[0].experiment:
            for student in group:
                temp = 0
                for student2 in group:
                    if student.id != student2.id:
                        temp += student.get_score(student2)
            scores.append(temp)
        else:
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


def improve_solution(groups: List[List[Student]]) -> List[List[Student]]:
    """
    כאן אנו מבצעים 'Swap' בין שני תלמידים בקבוצות שונות,
    כדי לשמור על גודל קבוצה קבוע.
    """
    new_groups = [g[:] for g in groups]  # עותק לקבוצות

    if len(new_groups) < 2:  # אם רק קבוצה אחת, אין מה להחליף
        return new_groups

    # בוחרים 2 קבוצות שונות באקראי
    idx1, idx2 = random.sample(range(len(new_groups)), 2)
    group1 = new_groups[idx1]
    group2 = new_groups[idx2]

    if len(group1) == 0 or len(group2) == 0:
        return new_groups

    # בוחרים תלמיד אחד מכל קבוצה
    i1 = random.randrange(len(group1))
    i2 = random.randrange(len(group2))

    # מבצעים את ההחלפה
    group1[i1], group2[i2] = group2[i2], group1[i1]

    return new_groups


def onlooker_bees(solutions: List[List[List[Student]]], scores: List[float]) -> None:
    total_score = sum(scores)
    if total_score == 0:
        # אם הכל אפס, אי אפשר לחשב הסתברויות
        return

    probabilities = [score / total_score for score in scores]
    num_solutions = len(solutions)

    for _ in range(num_solutions):
        # בוחרים פתרון לפי ההסתברויות
        chosen_idx = random.choices(range(num_solutions), probabilities)[0]
        old_solution = solutions[chosen_idx]
        old_score = scores[chosen_idx]

        new_solution = improve_solution(old_solution)
        new_score = calculate_diversity(new_solution)

        if new_score > old_score:
            solutions[chosen_idx] = new_solution
            scores[chosen_idx] = new_score


def abc_algorithm_with_prefrences(students: List[Student], num_groups: int, num_iterations: int = 3, limit: int = 3):
    """
    אלגוריתם ABC בסיסי:
    1. Initialization
    2. Employed Bees
    3. Onlooker Bees
    4. Scout Bees
    """
    global GLOBAL_MAX, GLOBAL_MAX_VAL
    # 1) יצירת פתרונות התחלתיים
    solutions = [initialize_groups(students[:], num_groups) for _ in range(num_groups)]
    scores = [calculate_diversity(sol) for sol in solutions]
    stagnation = [0] * num_groups  # מעקב אחרי מספר הפעמים ללא שיפור

    for iteration in range(num_iterations):
        # 2) Employed Bees
        for i in range(num_groups):
            old_score = scores[i]
            old_sol = solutions[i]

            new_sol = improve_solution(old_sol)
            new_score = calculate_diversity(new_sol)

            if new_score > old_score:
                solutions[i] = new_sol
                scores[i] = new_score
                stagnation[i] = 0
            else:
                stagnation[i] += 1

        # 3) Onlooker Bees
        onlooker_bees(solutions, scores)

        # 4) Scout Bees
        for i in range(num_groups):
            if stagnation[i] > limit:
                new_sol = initialize_groups(students[:], num_groups)
                solutions[i] = new_sol
                scores[i] = calculate_diversity(new_sol)
                stagnation[i] = 0
        # הדפסת מידע על הדור
        best_fitness = max(scores)
        if best_fitness > GLOBAL_MAX_VAL:
            GLOBAL_MAX_VAL = best_fitness
            GLOBAL_MAX = solutions[scores.index(GLOBAL_MAX_VAL)]
        print(f"Iteration {iteration + 1}, Best Fitness: {GLOBAL_MAX_VAL}")

    # בסוף, מחזירים את הפתרון הטוב ביותר
    return GLOBAL_MAX
