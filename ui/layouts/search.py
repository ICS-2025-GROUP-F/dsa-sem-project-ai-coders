# ui/layouts/search.py
from customtkinter import *
from data.database import students  # list of dicts

def init_ui(parent):
    frame = CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    CTkLabel(frame, text="🔍 Search Student", font=("Arial Bold", 18)).pack(pady=(0, 10))

    search_var = StringVar()

    entry = CTkEntry(frame, textvariable=search_var, placeholder_text="Enter name or ID...")
    entry.pack(pady=10)

    result_label = CTkLabel(frame, text="")
    result_label.pack(pady=10)

    def search():
        query = search_var.get().lower()
        results = [s for s in students if query in s["id"].lower() or query in s["name"].lower()]

        if not results:
            result_label.configure(text="No results found.", text_color="red")
        else:
            output = "\n".join(f"{s['id']} - {s['name']} | Avg: {s['average']:.2f}" for s in results)
            result_label.configure(text=output, text_color="white")

    CTkButton(frame, text="Search", command=search).pack(pady=10)
