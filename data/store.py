students = []

subject_names = ("Math", "English", "Science")
used_ids = set()


def add_student(student_id, name, marks):
    if student_id in used_ids:
        return False  # Duplicate
    student = {
        "id": student_id,
        "name": name,
        "marks": dict(zip(subject_names, marks)),
    }
    students.append(student)
    used_ids.add(student_id)
    return True


def get_all_students():
    return students


def get_student_by_id(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def compute_average(student):
    marks = student["marks"].values()
    return sum(marks) / len(marks)

students = []
SUBJECTS = ("Math", "English", "Science")

def add_student(sid, name, marks):
    if any(s["id"] == sid for s in students):
        return False
    student = {"id": sid, "name": name, "marks": marks}
    students.append(student)
    return True

def get_all_students():
    return students

def compute_average(student):
    return sum(student["marks"].values()) / len(student["marks"])

def compute_rankings():
    return sorted(students, key=compute_average, reverse=True)



def compute_rankings():
    return sorted(
        students,
        key=lambda s: compute_average(s),
        reverse=True
    )
