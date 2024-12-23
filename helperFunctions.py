import random
from student import Student
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

    :param min_val: הערך המינימלי האפשרי (int).
    :param max_val: הערך המקסימלי האפשרי (int).
    :param exclude: ערך שאינו יכול להיכלל בהעדפות (int).
    :return: רשימה של מספרים מועדפים (List[int]).
    """
    valid_values = [num for num in range(min_val, max_val + 1) if num != exclude]
    return random.sample(valid_values, 4 if len(valid_values) >= 4 else len(valid_values))

def generate_criteria_list(criteria_definitions: List[dict]) -> List[dict]:
    """
    יוצר רשימת קריטריונים עם ערכים רנדומליים.

    :param criteria_definitions: הגדרות הקריטריונים (List[dict]).
        כל קריטריון כולל:
        - name: שם הקריטריון (str).
        - type: סוג הקריטריון ("0-1", "0-10", "0-100").
    :return: רשימת קריטריונים עם ערכים רנדומליים (List[dict]).
    """
    def generate_value(criteria_type: str) -> float:
        """
        מייצר ערך רנדומלי בהתבסס על סוג הקריטריון.

        :param criteria_type: סוג הקריטריון (str).
        :return: ערך רנדומלי (float).
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
    Prints a table of student details.

    :param students: A list of student objects.
    """
    table_data = [
        [student.id, ', '.join(map(str, student.preferences)), f"{student.get_score():.2f}"]
        for student in students
    ]
    headers = ["ID", "Preferences", "Score"]
    print(tabulate(table_data, headers, tablefmt="grid"))
