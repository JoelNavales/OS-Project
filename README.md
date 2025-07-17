# OS Project 01 - CPU Scheduling Visualization

# Project Overview
# This Python GUI application visualizes the behavior of various CPU scheduling algorithms. Built using `tkinter`, the simulator provides an interactive way to input and generate processes, select scheduling algorithms, and observe how each one handles scheduling over time.

# First In First Out (FIFO)
# This program 
# 
# Shortest Job First (SJF)
# This program 
# 
# Shortest Remaining Time First (SRTF) - Preemptive
# This program 
# 
# Round Robin (RR)
# This program 
# 
# Multilevel Feedback Queue (MLFQ)
# This program 
# Features
- GUI using `tkinter`
- Manual process input (Name, Arrival Time, Burst Time)
- Random process generation
- Drop-down to select scheduling algorithm
- Visual Gantt chart (scrollable)
- Dynamic process table (Status, Completion, Turnaround, Response Time)
- Live action messages and CPU queue updates
- Average statistics displayed:
  - Waiting Time
  - Turnaround Time
  - Response Time
- Progress bar to simulate scheduling progress
- Dequeue and Clear buttons
  
# Instructions on how to use the simulator
**Add Processes**
   - Enter the process name, arrival time, and burst time.
   - Click "Add Process" or use "Generate Random" to auto-fill jobs.

**Choose An Algorithm**
   - Use the drop-down to select from FIFO, RR, SJF, SRTF, or MLFQ.
     
**Adjust Parameters (Optional)**  
   - Enter Time Slice for RR.
   - Set Allotment if using MLFQ.
     
**Run The Program**
   - Click "Run Scheduling" to visualize and calculate results.
**Analyze Results**
   - Gantt chart and job table update automatically.
   - Average turnaround, waiting, and response times are shown at the bottom.
# Member Roles and Contributions
# Joel Franco V Navales - GUI design,random job generation
# Justin Ramas - Backend logic, scheduling algorithm integration, statistics calculation
