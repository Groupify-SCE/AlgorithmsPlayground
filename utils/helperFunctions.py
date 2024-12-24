import random
import json
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
        file_name = f"students({num_students})_criteria({num_criteria}"
    students = []
    for student_id in range(1, num_students + 1):
        # מגריל העדפות רנדומליות
        preferences = generate_random_preferences(1, num_students, student_id)

        # מגדיל קריטריונים רנדומלים
        criteria = []
        for _ in range(num_criteria):
            criteria_type = random.choice(["0-1", "0-10", "0-100"])
            criteria_value = (
                random.choice([0, 1]) if criteria_type == "0-1" else
                random.randint(0, 10) if criteria_type == "0-10" else
                random.randint(0, 100)
            )
            criteria.append({
                "name": f"Criteria_{random.randint(1, 100)}",
                "type": criteria_type,
                "value": str(criteria_value)
            })

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
