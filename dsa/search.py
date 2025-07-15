from data.store import students


def linear_search_by_name(name):
    results = []
    for student in students:
        if name.lower() in student["name"].lower():
            results.append(student)
    return results


def binary_search_by_id(sorted_list, student_id):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid]["id"] == student_id:
            return sorted_list[mid]
        elif sorted_list[mid]["id"] < student_id:
            low = mid + 1
        else:
            high = mid - 1
    return None
