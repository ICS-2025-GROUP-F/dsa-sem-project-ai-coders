from data import student_manager

def top_students(n=3):
    students = student_manager.view_students()
    sorted_students = sorted(students, key=lambda s: s['average'], reverse=True)
    return sorted_students[:n]

def average_performance():
    students = student_manager.view_students()
    if not students:
        return 0
    total = sum(student['average'] for student in students)
    return total / len(students)
