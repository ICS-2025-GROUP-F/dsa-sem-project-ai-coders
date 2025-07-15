# ui/layouts/view.py
from customtkinter import *
from data.store import get_all_students

def init_ui(parent):
    frame = CTkScrollableFrame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    CTkLabel(frame, text="📋 All Students", font=("Arial Bold", 18)).pack(pady=(0, 10))

    students = get_all_students()
    if not students:
        CTkLabel(frame, text="No students found.").pack(pady=10)
        return

    for student in students:
        details = f"{student['student_id']} - {student['name']} | Avg: {student['average']:.2f}"
        CTkLabel(frame, text=details, anchor="w", justify="left").pack(fill="x", padx=10, pady=5)
