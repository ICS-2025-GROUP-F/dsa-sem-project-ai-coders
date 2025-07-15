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
from ui.layouts.manage import init_ui as manage_ui

# Import data store to initialize it
from data.store import student_manager

def main():
    # Apply theme
    apply_theme()

    # Create main application window
    app = CTk()
    app.geometry("1200x800")
    app.title("📊 Student Performance Tracker")
    
    # Create a notebook with tabs for different sections
    notebook = CTkTabview(app)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Add tabs
    home_tab = notebook.add("🏠 Home")
    register_tab = notebook.add("📝 Register")
    view_tab = notebook.add("🔍 View")
    manage_tab = notebook.add("✏️ Manage")
    search_tab = notebook.add("🔎 Search")
    analyze_tab = notebook.add("📊 Analyze")
    top3_tab = notebook.add("🏆 Top 3")
    
    # Variable to track if a tab's UI has been initialized
    initialized_tabs = {}
    last_tab = [None]  # Using a list to store mutable value
    
    # Function to initialize a tab when it's selected
    def check_tab_change():
        current_tab = notebook.get()
        if current_tab != last_tab[0]:  # Tab has changed
            last_tab[0] = current_tab
            
            if current_tab == "🏠 Home" and "Home" not in initialized_tabs:
                home_ui(home_tab)
                initialized_tabs["Home"] = True
            
            elif current_tab == "📝 Register" and "Register" not in initialized_tabs:
                register_ui(register_tab)
                initialized_tabs["Register"] = True
                
            elif current_tab == "🔍 View" and "View" not in initialized_tabs:
                view_tab_frame = CTkFrame(view_tab)
                view_tab_frame.pack(expand=True, fill="both")
                
                # Add a refresh button at the top
                refresh_frame = CTkFrame(view_tab_frame)
                refresh_frame.pack(fill="x", padx=10, pady=5)
                
                def refresh_view():
                    # Clear and reinitialize the view
                    for widget in view_content_frame.winfo_children():
                        widget.destroy()
                    view_ui(view_content_frame)
                    view_all_ui(view_content_frame)
                
                CTkButton(refresh_frame, text="🔄 Refresh", command=refresh_view).pack(anchor="e", padx=10)
                
                # Content frame for the actual view
                view_content_frame = CTkFrame(view_tab_frame)
                view_content_frame.pack(expand=True, fill="both")
                
                # Initialize views
                view_ui(view_content_frame)
                view_all_ui(view_content_frame)
                initialized_tabs["View"] = True
                
            elif current_tab == "✏️ Manage" and "Manage" not in initialized_tabs:
                manage_ui(manage_tab)
                initialized_tabs["Manage"] = True
                
            elif current_tab == "🔎 Search" and "Search" not in initialized_tabs:
                search_ui(search_tab)
                initialized_tabs["Search"] = True
                
            elif current_tab == "📊 Analyze" and "Analyze" not in initialized_tabs:
                analyze_frame = CTkFrame(analyze_tab)
                analyze_frame.pack(expand=True, fill="both")
                
                # Add a refresh button at the top
                refresh_frame = CTkFrame(analyze_frame)
                refresh_frame.pack(fill="x", padx=10, pady=5)
                
                def refresh_analyze():
                    # Clear and reinitialize the analyze view
                    for widget in analyze_content_frame.winfo_children():
                        widget.destroy()
                    analyze_ui(analyze_content_frame)
                
                CTkButton(refresh_frame, text="🔄 Refresh", command=refresh_analyze).pack(anchor="e", padx=10)
                
                # Content frame for the analyze view
                analyze_content_frame = CTkFrame(analyze_frame)
                analyze_content_frame.pack(expand=True, fill="both")
                
                # Initialize analyze view
                analyze_ui(analyze_content_frame)
                initialized_tabs["Analyze"] = True
                
            elif current_tab == "🏆 Top 3" and "Top3" not in initialized_tabs:
                top3_frame = CTkFrame(top3_tab)
                top3_frame.pack(expand=True, fill="both")
                
                # Add a refresh button at the top
                refresh_frame = CTkFrame(top3_frame)
                refresh_frame.pack(fill="x", padx=10, pady=5)
                
                def refresh_top3():
                    # Clear and reinitialize the top3 view
                    for widget in top3_content_frame.winfo_children():
                        widget.destroy()
                    top3_ui(top3_content_frame)
                
                CTkButton(refresh_frame, text="🔄 Refresh", command=refresh_top3).pack(anchor="e", padx=10)
                
                # Content frame for the top3 view
                top3_content_frame = CTkFrame(top3_frame)
                top3_content_frame.pack(expand=True, fill="both")
                
                # Initialize top3 view
                top3_ui(top3_content_frame)
                initialized_tabs["Top3"] = True
        
        # Continue checking every 100ms
        app.after(100, check_tab_change)
    
    # Status bar at the bottom
    status_bar = CTkFrame(app, height=20)
    status_bar.pack(side="bottom", fill="x")
    status_label = CTkLabel(status_bar, text="Ready")
    status_label.pack(side="left", padx=10)
    
    # Set the default tab and initialize it
    notebook.set("🏠 Home")
    home_ui(home_tab)  # Initialize first tab immediately
    initialized_tabs["Home"] = True
    last_tab[0] = "🏠 Home"
    
    # Start checking for tab changes
    app.after(100, check_tab_change)
    
    # Handle application close
    def on_close():
        student_manager.close()
        app.destroy()
        
    app.protocol("WM_DELETE_WINDOW", on_close)
    
    # Run the application
    app.mainloop()

if __name__ == "__main__":
    main()
