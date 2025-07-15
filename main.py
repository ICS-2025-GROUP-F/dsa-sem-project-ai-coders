import sys
import os

# Absolute path to the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from customtkinter import *
import tkinter as tk

# Import theme
from ui.themes.dark_theme import apply_theme

# Import layout components
from ui.layouts.home import init_ui as home_ui
from ui.layouts.register import init_ui as register_ui
from ui.layouts.view import init_ui as view_ui
from ui.layouts.view_all import init_ui as view_all_ui
from ui.layouts.search import init_ui as search_ui
from ui.layouts.analyze import init_ui as analyze_ui
from ui.layouts.top3 import init_ui as top3_ui

# Import data store to initialize it
from data.store import student_manager

def main():
    # Apply theme
    apply_theme()

    # Create main application window
    app = CTk()
    app.geometry("1000x800")
    app.title("📊 Student Performance Tracker")
    
    # Create a notebook with tabs for different sections
    notebook = CTkTabview(app)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Add tabs
    home_tab = notebook.add("🏠 Home")
    register_tab = notebook.add("📝 Register")
    view_tab = notebook.add("🔍 View")
    search_tab = notebook.add("🔎 Search")
    analyze_tab = notebook.add("📊 Analyze")
    top3_tab = notebook.add("🏆 Top 3")
    
    # Initialize the UI for each tab
    home_ui(home_tab)
    register_ui(register_tab)
    view_ui(view_tab)
    view_all_ui(view_tab)
    search_ui(search_tab)
    analyze_ui(analyze_tab)
    top3_ui(top3_tab)
    
    # Status bar at the bottom
    status_bar = CTkFrame(app, height=20)
    status_bar.pack(side="bottom", fill="x")
    status_label = CTkLabel(status_bar, text="Ready")
    status_label.pack(side="left", padx=10)
    
    # Set the default tab
    notebook.set("🏠 Home")
    
    # Handle application close
    def on_close():
        student_manager.close()
        app.destroy()
        
    app.protocol("WM_DELETE_WINDOW", on_close)
    
    # Run the application
    app.mainloop()

if __name__ == "__main__":
    main()
