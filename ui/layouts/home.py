
from customtkinter import *
from ui.layouts.register import init_ui as register_ui
from ui.layouts.view import init_ui as view_ui
from ui.layouts.analyze import init_ui as analyze_ui
from ui.layouts.search import init_ui as search_ui
from ui.layouts.top3 import init_ui as top3_ui

def init_ui(app):
    container = CTkFrame(app)
    container.pack(expand=True, fill="both", padx=20, pady=20)

    nav_frame = CTkFrame(container)
    nav_frame.pack(fill="x", pady=(0, 10))

    content_frame = CTkFrame(container)
    content_frame.pack(expand=True, fill="both")

    views = {
        "Register": register_ui,
        "View All": view_ui,
        "Analyze": analyze_ui,
        "Search": search_ui,
        "Top 3": top3_ui
    }

    def load_view(name):
        for widget in content_frame.winfo_children():
            widget.destroy()
        views[name](content_frame)

    segmented = CTkSegmentedButton(
        nav_frame,
        values=list(views.keys()),
        command=load_view
    )
    segmented.pack(pady=10, padx=20)
    segmented.set("Register")  # Load default
