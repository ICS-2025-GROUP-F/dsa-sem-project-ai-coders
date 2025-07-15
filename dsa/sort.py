def sort_by_name(students):
    """
    Sort students by name using the merge sort algorithm.
    """
    return merge_sort(students, key="name")

def sort_by_average(students):
    """
    Sort students by average score using the merge sort algorithm.
    Returns students in descending order (highest average first).
    """
    result = merge_sort(students, key="average")
    return list(reversed(result))  # Reverse to get descending order

def bubble_sort(students, key="name"):
    """
    Sort students by a specific key using bubble sort.
    This is an in-place sorting algorithm.
    """
    n = len(students)
    for i in range(n):
        for j in range(0, n-i-1):
            # Get the values to compare
            val1 = students[j].get(key, "")
            val2 = students[j+1].get(key, "")
            
            # Handle numeric values
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                if val1 > val2:
                    students[j], students[j+1] = students[j+1], students[j]
            # Handle string values
            else:
                if str(val1).lower() > str(val2).lower():
                    students[j], students[j+1] = students[j+1], students[j]
    
    return students

def merge_sort(students, key="name"):
    """
    Sort students by a specific key using merge sort.
    This returns a new sorted list without modifying the original.
    """
    if len(students) <= 1:
        return students.copy()  # Return a copy to avoid modifying the original

    mid = len(students) // 2
    left = merge_sort(students[:mid], key)
    right = merge_sort(students[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    """
    Merge two sorted lists based on a specific key.
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Get the values to compare
        val1 = left[i].get(key, "")
        val2 = right[j].get(key, "")
        
        # Handle numeric values
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if val1 <= val2:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # Handle string values
        else:
            if str(val1).lower() <= str(val2).lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
