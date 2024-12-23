class Student:
    """
    מחלקה לייצוג סטודנט, הכוללת נתונים כמו מזהה, שם, העדפות וקריטריונים לחישוב ציון.
    """
    def __init__(self, student_data: dict):
        """
        אתחול אובייקט סטודנט.

        :param student_data: מילון עם פרטי הסטודנט הכוללים:
            - id: מזהה הסטודנט (int).
            - name: שם הסטודנט (str).
            - preferences: רשימת העדפות (ברירת מחדל: רשימה ריקה).
            - criteria: רשימת קריטריונים לחישוב ציון (ברירת מחדל: רשימה ריקה).
        """
        self.id = student_data.get("id")
        self.name = student_data.get("name")
        self.preferences = student_data.get("preferences", [])  
        self.criteria = student_data.get("criteria", [])

    def get_score(self) -> float:
        """
        מחשב את הציון הכולל של הסטודנט על בסיס הקריטריונים.

        :return: הציון הכולל (float).
        """
        total_score = 0.0
        for criteria in self.criteria:
            criteria_type = criteria.get("type")
            value = float(criteria.get("value", 0))

            # חישוב הציון לפי סוג הקריטריון
            if criteria_type == "0-1":
                total_score += value * 100
            elif criteria_type == "0-10":
                total_score += value * 10
            elif criteria_type == "0-100":
                total_score += value

        return total_score

    def __repr__(self):
        """
        מציג את האובייקט בפורמט קריא.

        :return: מחרוזת המייצגת את האובייקט.
        """
        return f"Student(*{self.id}*, {self.preferences}, {self.get_score()})"
