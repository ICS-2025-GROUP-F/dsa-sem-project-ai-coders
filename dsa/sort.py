from data.store import compute_average

def sort_by_name(student_list):
    return sorted(student_list, key=lambda s: s["name"].lower())

def sort_by_average(student_list):
    return sorted(student_list, key=lambda s: compute_average(s), reverse=True)
