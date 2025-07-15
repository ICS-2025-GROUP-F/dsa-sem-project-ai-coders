from customtkinter import *
from data.store import get_all_students, compute_average, compute_rankings
from dsa.sort import sort_by_name, sort_by_average
from dsa.search import linear_search_by_name


def init_ui(app):
    frame = CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    CTkLabel(frame, text="📋 Student Records", font=("Arial", 18)).pack(pady=10)

    table_frame = CTkScrollableFrame(master=frame, height=300)
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_table(students):
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Header
        CTkLabel(table_frame, text="ID", width=100).grid(row=0, column=0, padx=5)
        CTkLabel(table_frame, text="Name", width=200).grid(row=0, column=1, padx=5)
        CTkLabel(table_frame, text="Average", width=100).grid(row=0, column=2, padx=5)

        for i, student in enumerate(students):
            CTkLabel(table_frame, text=student["id"]).grid(row=i+1, column=0, padx=5)
            CTkLabel(table_frame, text=student["name"]).grid(row=i+1, column=1, padx=5)
            CTkLabel(table_frame, text=f"{compute_average(student):.2f}").grid(row=i+1, column=2, padx=5)

    refresh_table(get_all_students())

    # 🧠 Top 3 Performers
    def show_top_3():
        top3 = compute_rankings()[:3]
        refresh_table(top3)

    # 🔍 Search by Name
    def search_student():
        name = search_entry.get()
        result = linear_search_by_name(name)
        refresh_table(result)

    # 🔀 Sorting Options
    def sort_by(option):
        if option == "Name":
            sorted_data = sort_by_name(get_all_students())
        else:
            sorted_data = sort_by_average(get_all_students())
        refresh_table(sorted_data)

    options_frame = CTkFrame(master=frame)
    options_frame.pack(pady=10)

    CTkButton(options_frame, text="🏆 Top 3", command=show_top_3).pack(side="left", padx=10)
    CTkButton(options_frame, text="🔄 Sort by Name", command=lambda: sort_by("Name")).pack(side="left", padx=10)
    CTkButton(options_frame, text="📊 Sort by Average", command=lambda: sort_by("Average")).pack(side="left", padx=10)

    search_entry = CTkEntry(master=options_frame, placeholder_text="Search by Name")
    search_entry.pack(side="left", padx=10)

    CTkButton(options_frame, text="🔍 Search", command=search_student).pack(side="left", padx=10)
