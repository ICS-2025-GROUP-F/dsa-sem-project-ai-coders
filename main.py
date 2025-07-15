import sys
import os

# Absolute path to the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from customtkinter import *

# Import theme
from ui.themes.dark_theme import apply_theme

# Import layout components
from ui.layouts.home import init_ui as home_ui
from ui.layouts.register import init_ui as register_ui
from ui.layouts.view import init_ui as view_ui
from ui.layouts.view_all import init_ui as view_all_ui

# (Optional) import widgets if needed
# from ui.widgets.search_bar import init_ui as search_ui

def main():
    apply_theme()  # Apply dark + green theme globally

    app = CTk()
    app.geometry("1000x800")
    app.title("📊 Student Performance Tracker")

    # Scrollable main container
    container = CTkScrollableFrame(master=app)
    container.pack(expand=True, fill="both", padx=20, pady=20)

    # Layout sections
    CTkLabel(container, text="🏠 Home", font=("Arial", 18, "bold")).pack(pady=10)
    home_ui(container)

    CTkLabel(container, text="📝 Register Student", font=("Arial", 18, "bold")).pack(pady=10)
    register_ui(container)

    CTkLabel(container, text="🔍 View Student", font=("Arial", 18, "bold")).pack(pady=10)
    view_ui(container)

    CTkLabel(container, text="📈 View All Students", font=("Arial", 18, "bold")).pack(pady=10)
    view_all_ui(container)

    app.mainloop()

if __name__ == "__main__":
    main()
