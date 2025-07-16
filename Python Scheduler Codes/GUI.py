import tkinter as tk
from tkinter import ttk, messagebox, StringVar, OptionMenu


class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator by: Navales & Ramas tandem <3")
        self.root.geometry("800x700")

        title = ttk.Label(root, text="CPU Scheduling", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        # Frame & Inputs
        input_frame = ttk.Frame(root)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Process name").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Arrival Time").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="Burst Time").grid(row=0, column=2, padx=5, pady=5)

        self.pid_entry = ttk.Entry(input_frame, width=10)
        self.arrival_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry = ttk.Entry(input_frame, width=10)

        self.pid_entry.grid(row=1, column=0, padx=5)
        self.arrival_entry.grid(row=1, column=1, padx=5)
        self.burst_entry.grid(row=1, column=2, padx=5)

        self.add_button = ttk.Button(input_frame, text="Add Process")
        self.add_button.grid(row=1, column=3, padx=5)

        # Dropdown Menu
        self.clicked = StringVar()
        self.clicked.set("FIFO")
        self.options = ["FIFO", "Round Robin", "SJF"]
        self.drop = OptionMenu(input_frame, self.clicked, *self.options)
        self.drop.grid(row=1, column=4, padx=5)

        # Time Slice & Allotment Time Inputs
        ttk.Label(input_frame, text="Time Slice").grid(row=0, column=5)
        self.time_slice_entry = ttk.Entry(input_frame, width=5)
        self.time_slice_entry.grid(row=1, column=5)

        ttk.Label(input_frame, text="Allotment").grid(row=0, column=6)
        self.allotment_entry = ttk.Entry(input_frame, width=5)
        self.allotment_entry.grid(row=1, column=6)

        # Gantt Chart Canvas
        self.gantt_chart = tk.Canvas(root, height=50, bg="white")
        self.gantt_chart.pack(pady=10, fill='x')

        # Action Message
        self.action_label = tk.Label(root, text="Action: Waiting for user...", fg="blue")
        self.action_label.pack(pady=5)

        # Process Status Treeview
        self.status_tree = ttk.Treeview(root, columns=("PID", "Status", "Progress", "Remaining", "Completion", "TAT", "RT"), show="headings")
        for col in self.status_tree["columns"]:
            self.status_tree.heading(col, text=col)
        self.status_tree.pack(pady=10)

        # Overall Progress Bar
        self.overall_progress = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
        self.overall_progress.pack(pady=10)

        # Next in Queue
        self.queue_label = tk.Label(root, text="Next in CPU Queue: None")
        self.queue_label.pack()

        # Average Statistics
        stats_frame = ttk.LabelFrame(root, text="Average Statistics")
        stats_frame.pack(pady=10, fill='x', padx=10)

        self.avg_wt = tk.Label(stats_frame, text="Average Waiting Time: 0.00")
        self.avg_tat = tk.Label(stats_frame, text="Average Turnaround Time: 0.00")
        self.avg_rt = tk.Label(stats_frame, text="Average Response Time: 0.00")

        self.avg_wt.pack(anchor='w')
        self.avg_tat.pack(anchor='w')
        self.avg_rt.pack(anchor='w')

        # Control Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.run_button = ttk.Button(button_frame, text="Run Scheduling", command=self.run_scheduling)
        self.clear_button = ttk.Button(button_frame, text="Clear Processes")
        self.exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)

        self.run_button.grid(row=0, column=0, padx=10)
        self.clear_button.grid(row=0, column=1, padx=10)
        self.exit_button.grid(row=0, column=2, padx=10)

    def run_scheduling(self):
        selected_algorithm = self.clicked.get()
        self.action_label.config(text=f"Action: Running {selected_algorithm} scheduling...")
        messagebox.showinfo("Selected Algorithm", f"Running {selected_algorithm} scheduling...")

        # Placeholder logic to demonstrate UI updates
        self.overall_progress["value"] = 50
        self.queue_label.config(text="Next in CPU Queue: P2, P3")
        self.avg_wt.config(text="Average Waiting Time: 5.00")
        self.avg_tat.config(text="Average Turnaround Time: 10.00")
        self.avg_rt.config(text="Average Response Time: 3.00")

        # Simulated Gantt Chart update
        self.gantt_chart.delete("all")
        x = 10
        sample_processes = [{"pid": "P1", "duration": 3}, {"pid": "P2", "duration": 5}]
        for p in sample_processes:
            width = p['duration'] * 40
            self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
            self.gantt_chart.create_text(x + width / 2, 25, text=p['pid'])
            x += width


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()