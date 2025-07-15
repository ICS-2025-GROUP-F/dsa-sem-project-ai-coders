from .student_manager import StudentManager

class ReportGenerator:
    """
    Generates reports and analytics based on student data.
    """
    
    def __init__(self, student_manager=None):
        self.student_manager = student_manager or StudentManager()
    
    def top_students(self, n=3):
        """Get top N students by average."""
        return self.student_manager.get_top_students(n)
    
    def average_performance(self):
        """Get average performance of all students."""
        return self.student_manager.get_average_performance()
        
    def get_grade_distribution(self):
        """Get distribution of grades among students."""
        grades = {'A+': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        for student in self.student_manager.get_all_students():
            grade = student.get_grade()
            if grade in grades:
                grades[grade] += 1
                
        return grades
    
    def subject_averages(self):
        """Get average mark for each subject."""
        subjects = StudentManager.SUBJECTS
        subject_totals = {subject: 0 for subject in subjects}
        subject_counts = {subject: 0 for subject in subjects}
        
        for student in self.student_manager.get_all_students():
            for subject, mark in student.marks.items():
                if subject in subject_totals:
                    subject_totals[subject] += mark
                    subject_counts[subject] += 1
        
        return {
            subject: (subject_totals[subject] / subject_counts[subject]) 
            if subject_counts[subject] > 0 else 0
            for subject in subjects
        }
