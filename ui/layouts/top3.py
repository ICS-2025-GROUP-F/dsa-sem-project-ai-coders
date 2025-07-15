

from customtkinter import *
from data.store import get_all_students

def init_ui(parent):
    frame = CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    CTkLabel(frame, text="🏆 Top 3 Performers", font=("Arial Bold", 18)).pack(pady=(0, 10))

    students = get_all_students()
    if len(students) < 1:
        CTkLabel(frame, text="No students available.").pack(pady=10)
        return

    # Sort students by average score descending
    sorted_students = sorted(students, key=lambda s: s["average"], reverse=True)[:3]

    for idx, student in enumerate(sorted_students, 1):
        info = f"{idx}. {student['name']} (ID: {student['student_id']}) - Avg: {student['average']:.2f}"
        CTkLabel(frame, text=info, anchor="w", justify="left").pack(fill="x", padx=10, pady=5)
