import mysql.connector  # Connect to MySQL
from collections import deque  # Queue for action history


class Student:
    """Represents a student with ID, name, marks, average, rank."""

    def __init__(self, student_id, name, marks=None):
        self.student_id = student_id
        self.name = name
        self.marks = marks or {}  # Dictionary: subject -> mark
        self.average = self.calculate_average()
        self.rank = 0

    def calculate_average(self):
        """Compute average marks."""
        if not self.marks:
            return 0.0
        return sum(self.marks.values()) / len(self.marks)

    def get_grade(self):
        """Return letter grade based on average."""
        avg = self.calculate_average()
        if avg >= 90:
            return 'A+'
        elif avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        else:
            return 'F'

    def to_dict(self):
        """Return student data as a dictionary."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'marks': self.marks,
            'average': self.average,
            'grade': self.get_grade()
        }


class DataManager:
    """Handles all student data operations using MySQL and in-memory data structures."""

    def __init__(self):
        # In-memory structures
        self.students = []  # List: all student objects
        self.student_ids = set()  # Set: unique student IDs
        self.action_history = deque(maxlen=10)  # Queue: last actions for undo

        self.subjects = ("Mathematics", "Science", "English")  # Tuple: read-only subjects

        # Connect to MySQL server (XAMPP)
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Use your XAMPP MySQL password if you set one
            database="student_db"
        )
        self.cursor = self.conn.cursor()

        self.create_table()
        self.load_all_students()

    def create_table(self):
        """Create the students table if it does not exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(100),
                math FLOAT,
                science FLOAT,
                english FLOAT
            )
        """)
        self.conn.commit()

    def load_all_students(self):
        """Load students from DB into list + set."""
        self.students.clear()
        self.student_ids.clear()

        self.cursor.execute("SELECT * FROM students")
        for row in self.cursor.fetchall():
            student_id, name, math, science, english = row
            marks = {
                "Mathematics": math,
                "Science": science,
                "English": english
            }
            student = Student(student_id, name, marks)
            self.students.append(student)
            self.student_ids.add(student_id)

    def add_student(self, student_id, name, marks):
        """Add student to DB and in-memory list."""
        if student_id in self.student_ids:
            raise ValueError("Student ID already exists!")

        sql = "INSERT INTO students (student_id, name, math, science, english) VALUES (%s, %s, %s, %s, %s)"
        values = (
            student_id,
            name,
            marks.get("Mathematics", 0),
            marks.get("Science", 0),
            marks.get("English", 0)
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

        student = Student(student_id, name, marks)
        self.students.append(student)
        self.student_ids.add(student_id)

        self.action_history.append(('ADD', student.to_dict()))
        return student

    def remove_student(self, student_id):
        """Delete student from DB and in-memory list."""
        sql = "DELETE FROM students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        self.conn.commit()

        for i, s in enumerate(self.students):
            if s.student_id == student_id:
                self.students.pop(i)
                self.student_ids.remove(student_id)
                self.action_history.append(('REMOVE', s.to_dict()))
                return True

        return False

    def update_student(self, student_id, name=None, marks=None):
        """Update student in DB and in-memory list."""
        student = self.find_student_by_id(student_id)
        if not student:
            return False

        old_data = student.to_dict()

        if name:
            student.name = name
        if marks:
            student.marks = marks

        sql = """
            UPDATE students
            SET name = %s, math = %s, science = %s, english = %s
            WHERE student_id = %s
        """
        values = (
            student.name,
            student.marks.get("Mathematics", 0),
            student.marks.get("Science", 0),
            student.marks.get("English", 0),
            student_id
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

        self.action_history.append(('UPDATE', old_data, student.to_dict()))
        return True

    def find_student_by_id(self, student_id):
        """Find a student by ID."""
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def search_students_by_name(self, name_part):
        """Search students by name (partial match)."""
        return [s for s in self.students if name_part.lower() in s.name.lower()]

    def calculate_ranks(self):
        """Sort students by average score and assign ranks."""
        sorted_list = sorted(self.students, key=lambda s: s.calculate_average(), reverse=True)
        for i, s in enumerate(sorted_list):
            s.rank = i + 1

    def get_all_students(self):
        """Return a copy of all student objects."""
        return self.students.copy()

    def close(self):
        """Close the DB connection."""
        self.cursor.close()
        self.conn.close()

