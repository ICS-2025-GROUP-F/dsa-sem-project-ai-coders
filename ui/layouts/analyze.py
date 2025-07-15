
from customtkinter import *
from data.database import students

def init_ui(parent):
    frame = CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    CTkLabel(frame, text="📊 Performance Analytics", font=("Arial Bold", 18)).pack(pady=(0, 10))

    if not students:
        CTkLabel(frame, text="No data available for analysis.").pack()
        return

    averages = [s["average"] for s in students]
    overall_avg = sum(averages) / len(averages)

    CTkLabel(frame, text=f"Overall Average: {overall_avg:.2f}").pack(pady=5)

    # Top 3 perfomers
    top_students = sorted(students, key=lambda s: s["average"], reverse=True)[:3]
    for i, s in enumerate(top_students, start=1):
        CTkLabel(frame, text=f"{i}. {s['name']} - {s['average']:.2f}").pack(pady=2)
