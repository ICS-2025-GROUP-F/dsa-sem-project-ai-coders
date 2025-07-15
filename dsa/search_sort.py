def linear_search(students, key, value):
    for student in students:
        if student[key].lower() == value.lower():
            return student
    return None

def binary_search(students, key, value):
    low = 0
    high = len(students) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = students[mid][key].lower()

        if mid_val == value.lower():
            return students[mid]
        elif mid_val < value.lower():
            low = mid + 1
        else:
            high = mid - 1
    return None

def bubble_sort(students, key):
    n = len(students)
    for i in range(n):
        for j in range(0, n-i-1):
            if students[j][key] > students[j+1][key]:
                students[j], students[j+1] = students[j+1], students[j]
    return students

def merge_sort(students, key):
    if len(students) <= 1:
        return students

    mid = len(students) // 2
    left = merge_sort(students[:mid], key)
    right = merge_sort(students[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    result = []
    while left and right:
        if left[0][key] <= right[0][key]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right) 
    return result