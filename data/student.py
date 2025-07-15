class Student:
    """
    Represents a student with ID, name, marks, average, and rank.
    """
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