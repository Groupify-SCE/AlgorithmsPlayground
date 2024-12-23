from utils.helperFunctions import generate_random_student_list, print_students_table

AMOUNT_OF_STUDENTS = 15
CRITERIA_LIST = [{"name": "GPA", "type": "0-100"}]

if __name__ == "__main__":
    students = generate_random_student_list(AMOUNT_OF_STUDENTS, CRITERIA_LIST)
    print_students_table(students)