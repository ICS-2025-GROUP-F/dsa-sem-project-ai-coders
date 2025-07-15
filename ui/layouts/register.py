
from customtkinter import *
from data.store import add_student, SUBJECTS
from tkinter.messagebox import showinfo, showerror

def init_ui(app):
    frame = CTkFrame(master=app)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    CTkLabel(frame, text="🎓 Register New Student", font=("Arial", 18)).pack(pady=10)

    form = CTkFrame(master=frame)
    form.pack(pady=10)

    id_entry = CTkEntry(form, placeholder_text="Student ID")
    id_entry.grid(row=0, column=1, padx=10, pady=5)
    CTkLabel(form, text="ID").grid(row=0, column=0, padx=10, pady=5)

    name_entry = CTkEntry(form, placeholder_text="Student Name")
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    CTkLabel(form, text="Name").grid(row=1, column=0, padx=10, pady=5)

    mark_entries = {}
    for idx, subject in enumerate(SUBJECTS):
        CTkLabel(form, text=subject).grid(row=2 + idx, column=0, padx=10, pady=5)
        mark_entries[subject] = CTkEntry(form, placeholder_text=f"{subject} marks")
        mark_entries[subject].grid(row=2 + idx, column=1, padx=10, pady=5)

    def on_submit():
        try:
            sid = id_entry.get().strip()
            name = name_entry.get().strip()
            marks = {subj: float(mark_entries[subj].get()) for subj in SUBJECTS}

            if not sid or not name:
                showerror("Error", "ID and Name are required")
                return

            success = add_student(sid, name, marks)
            if success:
                showinfo("Success", f"{name} added!")
                id_entry.delete(0, END)
                name_entry.delete(0, END)
                for entry in mark_entries.values():
                    entry.delete(0, END)
            else:
                showerror("Error", "Student ID already exists")
        except ValueError:
            showerror("Error", "Please enter valid numeric marks")

    CTkButton(frame, text="➕ Register Student", command=on_submit).pack(pady=15)
