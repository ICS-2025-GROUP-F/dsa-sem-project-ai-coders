from data.store import get_all_students


def linear_search_by_name(name):
    """
    Search students by name using linear search.
    Returns a list of matching students.
    """
    students = get_all_students()
    results = []

    for student in students:
        if name.lower() in student["name"].lower():
            results.append(student)

    return results


def linear_search_by_key(students, key, value):
    """
    Generic linear search by any key in the student dictionary.
    Returns the first matching student or None if not found.
    """
    for student in students:
        if key in student and str(student[key]).lower() == str(value).lower():
            return student
    return None


def binary_search_by_id(students, student_id):
    """
    Search students by ID using binary search.
    Assumes students are sorted by ID.
    Returns the matching student or None if not found.
    """
    low = 0
    high = len(students) - 1

    # Convert student_id to string for comparison
    student_id = str(student_id)

    while low <= high:
        mid = (low + high) // 2
        mid_id = students[mid].get("student_id", students[mid].get("id", ""))

        if mid_id == student_id:
            return students[mid]
        elif mid_id < student_id:
            low = mid + 1
        else:
            high = mid - 1

    return None


def binary_search_by_key(students, key, value):
    """
    Generic binary search by any key.
    Assumes students are sorted by the given key.
    Returns the matching student or None if not found.
    """
    low = 0
    high = len(students) - 1

    # Convert value to lowercase string for comparison
    value = str(value).lower()

    while low <= high:
        mid = (low + high) // 2
        mid_val = str(students[mid].get(key, "")).lower()

        if mid_val == value:
            return students[mid]
        elif mid_val < value:
            low = mid + 1
        else:
            high = mid - 1

    return None
