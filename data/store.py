from .student_manager import StudentManager

# Global instance of StudentManager that can be imported by other modules
student_manager = StudentManager()

# Define subject names for consistency
SUBJECTS = StudentManager.SUBJECTS

# Wrapper functions that use the student_manager

def add_student(student_id, name, marks):
    """Add a student to the database."""
    success, message = student_manager.add_student(student_id, name, marks)
    return success

def get_all_students():
    """Get all students."""
    return [student.to_dict() for student in student_manager.get_all_students()]

def get_student_by_id(student_id):
    """Get a student by ID."""
    student = student_manager.get_student(student_id)
    return student.to_dict() if student else None

def compute_average(student_dict):
    """Compute average for a student dictionary."""
    if isinstance(student_dict, dict) and 'marks' in student_dict:
        marks = student_dict['marks'].values()
        return sum(marks) / len(marks) if marks else 0
    return 0

def compute_rankings():
    """Compute rankings for all students."""
    student_manager.calculate_ranks()
    return [student.to_dict() for student in 
            sorted(student_manager.get_all_students(), 
                  key=lambda s: s.average, 
                  reverse=True)]

def delete_student(student_id):
    """Delete a student by ID."""
    success, message = student_manager.delete_student(student_id)
    return success

def update_student(student_id, name=None, marks=None):
    """Update a student."""
    success, message = student_manager.update_student(student_id, name, marks)
    return success

def undo_last_action():
    """Undo the last action."""
    return student_manager.undo_last_action()[0]

def close_connection():
    """Close the database connection."""
    student_manager.close()
