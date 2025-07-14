import tkinter as tk
from tkinter import ttk,messagebox

from matplotlib.pyplot import title


class CPUSchedluerGUI:
    def __init__(self,root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("600x400")

        #title
        title = ttk.Label(root, text="CPU Scheduling GUI", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        #Frame para sa input fields
        input_frame=ttk.Frame(root)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Process ID").grid(row=0, column=0, padx=5, pady=5)