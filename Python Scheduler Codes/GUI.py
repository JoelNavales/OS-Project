import tkinter as tk
from tkinter import ttk, messagebox, StringVar, OptionMenu
import random
import threading

class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator by: Navales & Ramas tandem <3")
        self.root.geometry("1920x1080")

        self.process_data = []  # to store process info
        self.process_items = {}  # map PID to Treeview item IDs

        title = ttk.Label(root, text="CPU Scheduling", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

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

        self.add_button = ttk.Button(input_frame, text="Add Process", command=self.getProcessInfo)
        self.add_button.grid(row=1, column=3, padx=5)

        self.dequeue_button = ttk.Button(input_frame, text="Dequeue Process", command=self.dequeueProcess)
        self.dequeue_button.grid(row=1, column=4, padx=5)

        self.clicked = StringVar()
        self.clicked.set("FIFO")
        self.options = ["FIFO", "RR", "SJF", "SRTF", "MLFQ"]
        self.drop = OptionMenu(input_frame, self.clicked, *self.options)
        self.drop.grid(row=1, column=5, padx=5)

        ttk.Label(input_frame, text="Time Slice").grid(row=0, column=6)
        self.time_slice_entry = ttk.Entry(input_frame, width=5)
        self.time_slice_entry.grid(row=1, column=6)

        ttk.Label(input_frame, text="Allotment").grid(row=0, column=7)
        self.allotment_entry = ttk.Entry(input_frame, width=5)
        self.allotment_entry.grid(row=1, column=7)

        ttk.Label(input_frame, text="No. of Jobs").grid(row=0, column=8)
        self.num_jobs_entry = ttk.Entry(input_frame, width=5)
        self.num_jobs_entry.grid(row=1, column=8)

        self.random_button = ttk.Button(input_frame, text="Generate Random", command=self.generateProcesses)
        self.random_button.grid(row=1, column=9, padx=5)

        gantt_frame = ttk.Frame(root)
        gantt_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.gantt_scroll = tk.Scrollbar(gantt_frame, orient='horizontal')
        self.gantt_chart = tk.Canvas(gantt_frame, height=60, bg="white", scrollregion=(0,0,3000,60), xscrollcommand=self.gantt_scroll.set)
        self.gantt_scroll.config(command=self.gantt_chart.xview)
        self.gantt_scroll.pack(side='bottom', fill='x')
        self.gantt_chart.pack(fill='x', expand=True)

        self.action_label = tk.Label(root, text="Action: Waiting for user...", fg="blue")
        self.action_label.pack(pady=5)

        self.status_tree = ttk.Treeview(root, columns=("PID", "Name", "Arrival", "Burst", "Completion", "Turn Around Time", "Response Time", "Status"), show="headings")
        for col in self.status_tree["columns"]:
            self.status_tree.heading(col, text=col)
        self.status_tree.pack(pady=10, fill='x')

        self.overall_progress = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate")
        self.overall_progress.pack(pady=10)

        self.queue_label = tk.Label(root, text="Next in CPU Queue: None")
        self.queue_label.pack()

        stats_frame = ttk.LabelFrame(root, text="Average Statistics")
        stats_frame.pack(pady=10, fill='x', padx=10)

        self.avg_wt = tk.Label(stats_frame, text="Average Waiting Time: 0.00")
        self.avg_tat = tk.Label(stats_frame, text="Average Turnaround Time: 0.00")
        self.avg_rt = tk.Label(stats_frame, text="Average Response Time: 0.00")

        self.avg_wt.pack(anchor='w')
        self.avg_tat.pack(anchor='w')
        self.avg_rt.pack(anchor='w')

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.run_button = ttk.Button(button_frame, text="Run Scheduling", command=self.start_thread)
        self.clear_button = ttk.Button(button_frame, text="Clear Processes", command=self.clearProcesses)
        self.exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)

        self.run_button.grid(row=0, column=0, padx=10)
        self.clear_button.grid(row=0, column=1, padx=10)
        self.exit_button.grid(row=0, column=2, padx=10)

    def start_thread(self):
        thread = threading.Thread(target=self.run_scheduling)
        thread.start()

    def getProcessInfo(self):
        try:
            name = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            pid = len(self.process_data) + 1
            data = {"PID": pid, "Name": name, "Arrival": arrival, "Burst": burst, "Completion": "-", "Turn Around Time": "-", "Response Time": "-", "Status": "Waiting"}
            self.process_data.append(data)
            item_id = self.status_tree.insert("", tk.END, values=(pid, name, arrival, burst, "-", "-", "-", "Waiting"))
            self.process_items[pid] = item_id
            self.action_label.config(text=f"Process '{name}' added.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for arrival and burst times.")

    def generateProcesses(self):
        try:
            count = int(self.num_jobs_entry.get())
            for i in range(count):
                pid = len(self.process_data) + 1
                name = f"Job{pid}"
                arrival = random.randint(0, 10)
                burst = random.randint(1, 10)
                data = {"PID": pid, "Name": name, "Arrival": arrival, "Burst": burst, "Completion": "-", "Turn Around Time": "-", "Response Time": "-", "Status": "Waiting"}
                self.process_data.append(data)
                item_id = self.status_tree.insert("", tk.END, values=(pid, name, arrival, burst, "-", "-", "-", "Waiting"))
                self.process_items[pid] = item_id
            self.action_label.config(text=f"{count} random processes generated.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for number of jobs.")

    def dequeueProcess(self):
        selected = self.status_tree.selection()
        for item in selected:
            self.status_tree.delete(item)
            for pid, item_id in list(self.process_items.items()):
                if item_id == item:
                    self.process_items.pop(pid)
                    break

    def clearProcesses(self):
        self.status_tree.delete(*self.status_tree.get_children())
        self.process_data.clear()
        self.process_items.clear()
        self.gantt_chart.delete("all")
        self.overall_progress["value"] = 0
        self.queue_label.config(text="Next in CPU Queue: None")
        self.avg_wt.config(text="Average Waiting Time: 0.00")
        self.avg_tat.config(text="Average Turnaround Time: 0.00")
        self.avg_rt.config(text="Average Response Time: 0.00")
        self.action_label.config(text="All processes cleared.")

    def run_scheduling(self):
        algo = self.clicked.get()
        self.action_label.config(text=f"Action: Running {algo} scheduling...")
        for data in self.process_data:
            pid = data["PID"]
            completion = data["Arrival"] + data["Burst"]
            tat = completion - data["Arrival"]
            rt = 0  # Assume na 0 kai wa pai data
            data["Completion"] = completion
            data["Turn Around Time"] = tat
            data["Response Time"] = rt
            data["Status"] = "Completed"
            item_id = self.process_items[pid]
            self.status_tree.item(item_id, values=(
                pid, data["Name"], data["Arrival"], data["Burst"],
                completion, tat, rt, "Completed"
            ))
        self.action_label.config(text=f"Scheduling complete using {algo}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()
