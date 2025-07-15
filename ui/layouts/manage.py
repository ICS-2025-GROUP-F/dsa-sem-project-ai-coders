from customtkinter import *
from data.store import get_all_students, get_student_by_id, update_student, delete_student
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import ttk

def init_ui(parent):
    frame = CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    CTkLabel(frame, text="✏️ Manage Students", font=("Arial Bold", 18)).pack(pady=(0, 10))
    
    # Create two frames - one for the student list, one for editing
    list_frame = CTkFrame(frame)
    list_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    
    edit_frame = CTkFrame(frame)
    edit_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    
    # Selected student
    selected_student = {"id": None}
    
    # Student list with scrollbar
    list_label = CTkLabel(list_frame, text="Select a student to edit:", anchor="w")
    list_label.pack(fill="x", padx=5, pady=5)
    
    # Create a treeview to display students
    tree_frame = CTkFrame(list_frame)
    tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # We need to use regular ttk Treeview since CustomTkinter doesn't have one
    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Average"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Average", text="Average")
    tree.column("ID", width=80)
    tree.column("Name", width=150)
    tree.column("Average", width=80)
    tree.pack(fill="both", expand=True, side="left")
    
    # Add scrollbar
    scrollbar = CTkScrollbar(tree_frame, command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Edit form
    edit_label = CTkLabel(edit_frame, text="Edit Student Details:", anchor="w")
    edit_label.pack(fill="x", padx=5, pady=5)
    
    edit_form = CTkFrame(edit_frame)
    edit_form.pack(padx=5, pady=5, fill="x")
    
    # Student ID (read-only)
    CTkLabel(edit_form, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    id_var = StringVar()
    id_entry = CTkEntry(edit_form, textvariable=id_var, state="readonly", width=200)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Student Name
    CTkLabel(edit_form, text="Student Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_var = StringVar()
    name_entry = CTkEntry(edit_form, textvariable=name_var, width=200)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    # Marks Frame
    marks_frame = CTkFrame(edit_frame)
    marks_frame.pack(padx=5, pady=5, fill="x")
    
    CTkLabel(marks_frame, text="Subject Marks:", anchor="w").pack(fill="x", padx=5, pady=5)
    
    # Dictionary to store mark entries
    mark_entries = {}
    subjects = ["Mathematics", "Science", "English"]
    
    # Create entry fields for each subject
    for i, subject in enumerate(subjects):
        subject_frame = CTkFrame(marks_frame)
        subject_frame.pack(fill="x", padx=5, pady=2)
        
        CTkLabel(subject_frame, text=f"{subject}:", width=100).pack(side="left", padx=5)
        mark_var = StringVar()
        mark_entry = CTkEntry(subject_frame, textvariable=mark_var, width=100)
        mark_entry.pack(side="left", padx=5)
        mark_entries[subject] = mark_var
    
    # Buttons Frame
    buttons_frame = CTkFrame(edit_frame)
    buttons_frame.pack(pady=10, fill="x")
    
    def update_selected_student():
        if selected_student["id"] is None:
            showerror("Error", "No student selected")
            return
        
        try:
            # Get updated values
            student_id = id_var.get()
            name = name_var.get()
            
            # Validate name
            if not name.strip():
                showerror("Error", "Name cannot be empty")
                return
                
            # Get and validate marks
            marks = {}
            for subject, var in mark_entries.items():
                try:
                    mark = float(var.get())
                    if mark < 0 or mark > 100:
                        showerror("Error", f"{subject} mark must be between 0 and 100")
                        return
                    marks[subject] = mark
                except ValueError:
                    showerror("Error", f"Invalid mark for {subject}")
                    return
            
            # Update student
            success = update_student(student_id, name, marks)
            
            if success:
                showinfo("Success", "Student updated successfully")
                refresh_student_list()
            else:
                showerror("Error", "Failed to update student")
                
        except Exception as e:
            showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_selected_student():
        if selected_student["id"] is None:
            showerror("Error", "No student selected")
            return
            
        if askyesno("Confirm", f"Delete student {selected_student['name']}?"):
            success = delete_student(selected_student["id"])
            if success:
                showinfo("Success", "Student deleted successfully")
                clear_form()
                refresh_student_list()
            else:
                showerror("Error", "Failed to delete student")
    
    def clear_form():
        id_var.set("")
        name_var.set("")
        for var in mark_entries.values():
            var.set("")
        selected_student["id"] = None
    
    # Add buttons
    update_btn = CTkButton(buttons_frame, text="Update Student", command=update_selected_student)
    update_btn.pack(side="left", padx=5)
    
    delete_btn = CTkButton(buttons_frame, text="Delete Student", fg_color="red", command=delete_selected_student)
    delete_btn.pack(side="left", padx=5)
    
    clear_btn = CTkButton(buttons_frame, text="Clear Form", command=clear_form)
    clear_btn.pack(side="left", padx=5)
    
    # Function to populate student list
    def refresh_student_list():
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Get all students
        students = get_all_students()
        
        # Add students to the tree
        for student in students:
            tree.insert("", "end", values=(
                student["student_id"], 
                student["name"], 
                f"{student['average']:.2f}"
            ))
    
    # Function to load student details into the form
    def load_student_details(event):
        selected_item = tree.focus()
        if not selected_item:
            return
            
        # Get student ID from selected row
        student_id = tree.item(selected_item, "values")[0]
        student = get_student_by_id(student_id)
        
        if student:
            # Store selected student
            selected_student["id"] = student["student_id"]
            selected_student["name"] = student["name"]
            
            # Update form fields
            id_var.set(student["student_id"])
            name_var.set(student["name"])
            
            # Update mark entries
            for subject, mark in student["marks"].items():
                if subject in mark_entries:
                    mark_entries[subject].set(str(mark))
    
    # Bind tree selection event
    tree.bind("<<TreeviewSelect>>", load_student_details)
    
    # Add refresh button to list frame
    refresh_btn = CTkButton(list_frame, text="🔄 Refresh List", command=refresh_student_list)
    refresh_btn.pack(pady=10)
    
    # Initial load of student list
    refresh_student_list()
    
    return frame 