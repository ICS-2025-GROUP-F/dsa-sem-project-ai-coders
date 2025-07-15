from collections import deque
from .student import Student
from .database import get_db_connection

class StudentManager:
    """
    Handles all student data operations using SQLite and in-memory data structures.
    Implements four data structures:
    1. List - For storing all student objects
    2. Dictionary - For storing student data
    3. Set - For tracking unique student IDs
    4. Queue - For action history to support undo functionality
    """
    SUBJECTS = ("Mathematics", "Science", "English")
    
    def __init__(self):
        # In-memory data structures
        self.students = []  # List: all student objects
        self.students_dict = {}  # Dictionary: id -> student
        self.student_ids = set()  # Set: unique student IDs
        self.action_history = deque(maxlen=10)  # Queue: last actions for undo
        
        # Connect to database
        self.conn = get_db_connection()
        self.load_all_students()
    
    def load_all_students(self):
        """Load students from DB into memory data structures."""
        self.students.clear()
        self.students_dict.clear()
        self.student_ids.clear()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT student_id, name, math, science, english FROM students")
        
        for row in cursor.fetchall():
            student_id = row['student_id']
            name = row['name']
            marks = {
                "Mathematics": row['math'] if row['math'] is not None else 0,
                "Science": row['science'] if row['science'] is not None else 0,
                "English": row['english'] if row['english'] is not None else 0
            }
            
            student = Student(student_id, name, marks)
            self.students.append(student)
            self.students_dict[student_id] = student
            self.student_ids.add(student_id)
    
    def add_student(self, student_id, name, marks):
        """Add student to DB and in-memory data structures."""
        if student_id in self.student_ids:
            return False, "Student ID already exists!"
        
        # Validate marks dictionary
        if not isinstance(marks, dict):
            return False, "Marks must be a dictionary!"
        
        # Add to database
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO students (student_id, name, math, science, english) VALUES (?, ?, ?, ?, ?)",
            (
                student_id,
                name,
                marks.get("Mathematics", 0),
                marks.get("Science", 0),
                marks.get("English", 0)
            )
        )
        self.conn.commit()
        
        # Add to in-memory data structures
        student = Student(student_id, name, marks)
        self.students.append(student)
        self.students_dict[student_id] = student
        self.student_ids.add(student_id)
        
        # Record action for undo
        self.action_history.append(('ADD', student_id))
        
        return True, "Student added successfully!"
    
    def get_student(self, student_id):
        """Get a student by ID."""
        return self.students_dict.get(student_id)
    
    def get_all_students(self):
        """Return all students."""
        return self.students
    
    def update_student(self, student_id, name=None, marks=None):
        """Update student in DB and in-memory data structures."""
        if student_id not in self.student_ids:
            return False, "Student not found!"
            
        student = self.students_dict[student_id]
        old_data = student.to_dict()
        
        # Update data
        if name:
            student.name = name
        if marks:
            student.marks = marks
            student.average = student.calculate_average()
        
        # Update database
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE students SET name=?, math=?, science=?, english=? WHERE student_id=?",
            (
                student.name,
                student.marks.get("Mathematics", 0),
                student.marks.get("Science", 0),
                student.marks.get("English", 0),
                student_id
            )
        )
        self.conn.commit()
        
        # Record action for undo
        self.action_history.append(('UPDATE', student_id, old_data))
        
        return True, "Student updated successfully!"
    
    def delete_student(self, student_id):
        """Delete student from DB and in-memory data structures."""
        if student_id not in self.student_ids:
            return False, "Student not found!"
            
        # Get student data before deletion for undo
        student = self.students_dict[student_id]
        old_data = student.to_dict()
        
        # Delete from database
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        self.conn.commit()
        
        # Delete from in-memory data structures
        self.students = [s for s in self.students if s.student_id != student_id]
        del self.students_dict[student_id]
        self.student_ids.remove(student_id)
        
        # Record action for undo
        self.action_history.append(('DELETE', student_id, old_data))
        
        return True, "Student deleted successfully!"
    
    def search_students_by_name(self, name_part):
        """Search students by partial name match."""
        if not name_part:
            return []
        return [s for s in self.students if name_part.lower() in s.name.lower()]
    
    def get_top_students(self, n=3):
        """Get top N students by average."""
        sorted_students = sorted(self.students, key=lambda s: s.calculate_average(), reverse=True)
        return sorted_students[:n]
        
    def calculate_ranks(self):
        """Sort students by average score and assign ranks."""
        sorted_students = sorted(self.students, key=lambda s: s.calculate_average(), reverse=True)
        for i, student in enumerate(sorted_students):
            student.rank = i + 1
    
    def get_average_performance(self):
        """Calculate average performance of all students."""
        if not self.students:
            return 0
        return sum(s.calculate_average() for s in self.students) / len(self.students)
    
    def undo_last_action(self):
        """Undo last action if possible."""
        if not self.action_history:
            return False, "No actions to undo"
            
        action = self.action_history.pop()
        action_type = action[0]
        
        if action_type == 'ADD':
            student_id = action[1]
            return self.delete_student(student_id)
        
        elif action_type == 'DELETE':
            student_id = action[1]
            old_data = action[2]
            return self.add_student(student_id, old_data['name'], old_data['marks'])
        
        elif action_type == 'UPDATE':
            student_id = action[1]
            old_data = action[2]
            return self.update_student(student_id, old_data['name'], old_data['marks'])
        
        return False, "Unknown action type"
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
