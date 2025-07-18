# OS Project 01 - CPU Scheduling Visualization

# Project Overview
This Python GUI application visualizes the behavior of various CPU scheduling algorithms. Built using `tkinter`, the simulator provides an interactive way to input and generate processes, select scheduling algorithms, and observe how each one handles scheduling over time.

# Sample Output
<img width="1600" height="860" alt="image" src="https://github.com/user-attachments/assets/d770cb2c-a2d7-4e34-9b2b-9bebe5b556d4" />

The image shows the simulator run by generating 5 random process and using the `RR` scheduling algorithm.

# Simulator Features
- Scheduling algorithms implemented are:
  - First In First Out (`FIFO`)
    - Runs the jobs according to their `Arrival Time`.
  - Shortest Job First (`SJF`)
    - Runs the jobs according to their `Arrival Time` and `Burst Time`, running the shortest `Burst Time` first.
  - Shortest Remaining Time First (`SRTF`) - Preemptive
    - Runs the same as `SJF` but in `SRTF`, if the `Burst Time` of the job in queue is shorter than the currently running job, it switches to the shorter `Burst Time`.
  - Round Robin (`RR`)
    - Runs the jobs according to their `Arrival Time` equally by giving each job their own `Time Slice`.
  - Multilevel Feedback Queue (`MLFQ`)
    - Puts jobs on priority queues (with `Q0` the highest queue) and runs them according to their `Arrival Time`. Jobs on the highest priority queue are run first, and each job gets their `Time Slice` and `Allotment Time` in each queue.
- GUI created using `tkinter`
- Manual process input (`Process Name`, `Arrival Time`, `Burst Time`, `Time Slice`, and `Allotment Time`)
- Random process generation
- Drop-down menu to select scheduling algorithm
- Visual Gantt chart (scrollable)
- Dynamic process table (`Status`, `Completion Time`, `Turnaround Time`, `Response Time`)
- Live action messages and CPU queue updates
- Average statistics displayed:
  - `Waiting Time`
  - `Turnaround Time`
  - `Response Time`
- Progress bar to simulate scheduling progress
- Dequeue and Clear buttons

  
# Instructions on how to use the simulator
<img width="895" height="267" alt="image" src="https://github.com/user-attachments/assets/94a3880c-690d-477e-b7ba-c82e3c13dcf1" />

**Add and Remove Processes**
- You can add processes by:
   - Enter the number of jobs and click "Generate Random" to auto-fill jobs.
   - Enter the Process Name (optional), Arrival Time, and Burst Time and click "Add Process" to add job to the list.
- You can remove processes by:
   - Select which job to remove by clicking on the Job Table and then clicking "Dequeue Process".
   - Clicking the "Clear Processes" to remove all processes and data from the simulator.

**Choose An Algorithm**
   - Use the drop-down to select from `FIFO`, `RR`, `SJF`, `SRTF`, or `MLFQ`.
     
**Adjust Parameters (Optional)**  
   - Enter Time Slice for `RR` and `MLFQ`.
   - Set Allotment if using `MLFQ`.
     
**Run The Program**

<img width="392" height="59" alt="image" src="https://github.com/user-attachments/assets/1ef281bf-7276-499b-820d-80c8f179246c" />

   - Click "Run Scheduling" to visualize and calculate results.
     
**Analyze Results**

<img width="1600" height="607" alt="image" src="https://github.com/user-attachments/assets/6ff57c1c-043a-4be9-b4a1-00890f5cd368" />

   - The Gantt Chart and Job Table update at run-time. The Gantt Chart shows if the CPU is idle or which job run in every `Time Tick` by showing the job's PID.
   - Average `Turnaround`, `Waiting`, and `Response` Times are shown at the bottom-left corner of the simulator.

# Known Bugs
- Wrong computation for the Turnaround Time.
- Next job in queue indicator sometimes not showing the next job in queue.

# Member Roles and Contributions
- Joel Franco V Navales : GUI design,random job generation.
- Justin Ramas : Backend logic, scheduling algorithm integration, statistics calculation.
