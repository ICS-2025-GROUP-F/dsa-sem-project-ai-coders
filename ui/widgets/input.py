# ui/widgets/inputs.py
from customtkinter import *

def labeled_entry(master, label_text, placeholder):
    frame = CTkFrame(master)
    frame.pack(fill="x", pady=5)

    CTkLabel(frame, text=label_text).pack(anchor="w")
    entry = CTkEntry(frame, placeholder_text=placeholder)
    entry.pack(fill="x", padx=5)

    return entry

def submit_button(master, text, command):
    return CTkButton(master, text=text, command=command)
