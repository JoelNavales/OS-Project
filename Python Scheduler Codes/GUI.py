import tkinter as tk
from tkinter import ttk, messagebox, StringVar, OptionMenu

import random
import sys
from time import sleep
import threading

numQueues = 4

#User Input
timeSlice = 1

quantum = {}
for i in range(numQueues):
    quantum[i] = int(timeSlice)

allotmentSlice = 1
allotment = {}
for i in range(numQueues):
    allotment[i] = int(allotmentSlice)

hiQueue = 0
ioDone = {}

jobnum = 0
joblist = {}

class CPUSchedulerGUI:

    def updateNextQueue(self, algo_runlist):
        if len(algo_runlist) > 1:
            self.queue_label.config(text="PID of Next in CPU Queue: " + str(algo_runlist[1][0]))
        elif len(algo_runlist) >= 0:
            self.queue_label.config(text="PID of Next in CPU Queue: N/A")

    def updateOverallProgress(self, totalBurstTime, progress, ranfor):
        progress+=ranfor
        value = (progress / totalBurstTime) * 100
        self.overall_progress["value"] = value

        return progress

    def start_thread(self):
        thread = threading.Thread(target=self.run_scheduling)
        thread.start()

    def generateProcesses(self):
        #numberOfJobs = GET FROM USER
        numberOfJobs = 5

        global joblist
        global jobnum

        for jobnum in range(0,numberOfJobs):
            pid = jobnum + 5
            processName = "Job " + str(jobnum)
            arrivalTime = int(10 * random.random()) + 1
            burstTime = int(10 * random.random()) + 1

            joblist[jobnum] = {'currPri':hiQueue, 'ticksLeft':quantum[hiQueue],
                    'allotLeft':allotment[hiQueue], 'arrivalTime':arrivalTime,
                    'burstTime':burstTime, 'timeLeft':burstTime, 'firstRun':-1, 'pid': pid, 'processName': processName} 
            
            print('Got entry Process Name:', processName, 'Arrival Time:', str(arrivalTime), 'Burst Time: ', str(burstTime))
            self.status_tree.insert("", tk.END, values=(pid, "WAITING"))
        
        self.action_label.config(text = "Processes has been successfully added to the queue.")

    def clearProcesses(self):
        global joblist

        for i in self.status_tree.get_children():
            self.status_tree.delete(i)
        self.status_tree.update()

        joblist = {}

    def getProcessInfo(self):
        global jobnum
        global joblist

        processName = self.pid_entry.get()
        if processName == '':
            processName = "Job " + str(jobnum)
        arrivalTime = self.arrival_entry.get()
        burstTime = self.burst_entry.get()


        pid = jobnum + 5

        try:
            arrivalTime = int(arrivalTime)

            if arrivalTime < 0:
                messagebox.showerror("Error", "Please enter an Arrival Time greater than  or equal to 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid Arrival Time integer", icon = 'error')
            return
        
        try:
            burstTime = int(burstTime)

            if burstTime <= 0:
                messagebox.showerror("Error", "Please enter a Burst Time greater than 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid Burst Time integer", icon = 'error')
            return

        print('Got entry Process Name:', processName, 'Arrival Time:', str(arrivalTime), 'Burst Time: ', str(burstTime))

        joblist[jobnum] = {'currPri':hiQueue, 'ticksLeft':quantum[hiQueue],
                    'allotLeft':allotment[hiQueue], 'arrivalTime':arrivalTime,
                    'burstTime':burstTime, 'timeLeft':burstTime, 'firstRun':-1, 'pid': pid, 'processName': processName} 
        
        self.status_tree.insert("", tk.END, values=(pid))
        self.action_label.config(text = processName +  " has been successfully added to the queue.")
        
        jobnum+=1

    def run_scheduling(self):
        global joblist

        self.gantt_chart.delete("all")
        selected_algorithm = self.clicked.get()
        self.action_label.config(text=f"Action: Running {selected_algorithm} scheduling...")
        messagebox.showinfo("Selected Algorithm", f"Running {selected_algorithm} scheduling...")

        if selected_algorithm == "FIFO":
            FIFO_joblist = []
            progress = 0.0
            totalBurstTime = 0

            for e in joblist:
                pid = joblist[e]['pid']
                jobnum = e
                processName = joblist[e]['processName']
                arrivalTime = joblist[e]['arrivalTime']
                burstTime = joblist[e]['burstTime']

                FIFO_joblist.append([pid, jobnum, processName, arrivalTime, burstTime])
                print('[PID', str(pid), '] Jobnum', str(jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            FIFO_joblist = sorted(FIFO_joblist, key=lambda e: e[3])

            for b in FIFO_joblist:
                totalBurstTime += b[4]

            print('Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = 1.0
            jobcount = len(FIFO_joblist)
            x = 10

            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1

            templist = []
            for e in FIFO_joblist:
                templist.append(e)

            runlist = []
            # runlist.append(templist[0])
            # templist.pop(0)

            index = 0
            for e in templist:
                if 0 == e[3]:
                    runlist.append(templist[index])
                    templist.pop(index)
                    break
                    
                index+=1

            thetime  = 0.0
            while jobcount > 0:  
                if len(runlist) != 0:
                    jobnum = runlist[0][1]

                    if response[runlist[0][1]] == -1:
                        response[runlist[0][1]] = thetime

                    currwait = thetime - lastran[runlist[0][1]]
                    wait[runlist[0][1]] += currwait

                if len(runlist) == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (thetime, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                elif runlist[0][4] > quantum:
                    runlist[0][4] -= quantum
                    ranfor = quantum

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    print('  [ time %3d ] Run job %3d for %.2f secs' % (thetime, runlist[0][1], ranfor))
                    
                elif runlist[0][4] <= quantum:
                    ranfor = runlist[0][4]
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, runlist[0][1], ranfor, thetime + ranfor))
                    turnaround[runlist[0][1]] = thetime + ranfor

                    #Update Gantt Chart
                    
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)
                    
                    runlist.pop(0)
                    jobcount -= 1
                    
                thetime += ranfor
                lastran[jobnum] = thetime

                index = 0
                for e in templist:
                    if thetime >= e[3]:
                        runlist.append(templist[index])
                        templist.pop(index)
                        break
                    
                    index+=1
                
                sleep(0.3)

            print('\nFinal statistics:')

            turnaroundTotal = 0.0
            waitTotal       = 0.0
            responseTotal   = 0.0

            for i in range(0,len(FIFO_joblist)):
                turnaroundTotal += turnaround[i]
                responseTotal += response[i]
                waitTotal += wait[i]
                print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i]))

            count = len(FIFO_joblist)
            avgResponseTime = responseTotal/count
            avgTurnaroundTime = turnaroundTotal/count
            avgWaitTime = waitTotal/count
            
            print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))

            self.avg_wt.config(text="Average Waiting Time: " + str(avgWaitTime))
            self.avg_tat.config(text="Average Turnaround Time: " + str(avgTurnaroundTime))
            self.avg_rt.config(text="Average Response Time: " + str(avgResponseTime))

            


        elif selected_algorithm == "SJF":
            SJF_joblist = []
            progress = 0.0
            totalBurstTime = 0

            for e in joblist:
                pid = joblist[e]['pid']
                jobnum = e
                processName = joblist[e]['processName']
                arrivalTime = joblist[e]['arrivalTime']
                burstTime = joblist[e]['burstTime']

                SJF_joblist.append([pid, jobnum, processName, arrivalTime, burstTime])
                print('[PID', str(pid), '] Jobnum', str(jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            SJF_joblist = sorted(SJF_joblist, key=lambda e: (e[3], e[4]))

            for b in SJF_joblist:
                totalBurstTime += b[4]

            print('Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = 1.0
            jobcount = len(SJF_joblist)
            x = 10

            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1

            templist = []
            for e in SJF_joblist:
                templist.append(e)

            runlist = []
            # runlist.append(templist[0])
            # templist.pop(0)

            index = 0
            for e in templist:
                if 0 == e[3]:
                    runlist.append(templist[index])
                    templist.pop(index)
                    break
                    
                index+=1

            thetime  = 0.0
            while jobcount > 0:  
                if len(runlist) != 0:
                    jobnum =  runlist[0][1]
                    if response[runlist[0][1]] == -1:
                        response[runlist[0][1]] = thetime

                    currwait = thetime - lastran[runlist[0][1]]
                    wait[runlist[0][1]] += currwait

                if len(runlist) == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (thetime, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                elif runlist[0][4] > quantum:
                    runlist[0][4] -= quantum
                    ranfor = quantum

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    print('  [ time %3d ] Run job %3d for %.2f secs' % (thetime, runlist[0][1], ranfor))
                    
                elif runlist[0][4] <= quantum:
                    ranfor = runlist[0][4]
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, runlist[0][1], ranfor, thetime + ranfor))
                    turnaround[runlist[0][1]] = thetime + ranfor

                    #Update Gantt Chart
                    
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)
                    
                    runlist.pop(0)

                    if len(runlist) != 0:
                        runlist = sorted(runlist, key=lambda e: e[4])
                    jobcount -= 1
                    
                thetime += ranfor
                lastran[jobnum] = thetime

                index = 0
                for e in templist:
                    if thetime >= e[3]:
                        runlist.append(templist[index])
                        templist.pop(index)
                        break
                    
                    index+=1
                
                sleep(0.3)

            print('\nFinal statistics:')

            turnaroundTotal = 0.0
            waitTotal       = 0.0
            responseTotal   = 0.0

            for i in range(0,len(SJF_joblist)):
                turnaroundTotal += turnaround[i]
                responseTotal += response[i]
                waitTotal += wait[i]
                print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i]))

            count = len(SJF_joblist)
            avgResponseTime = responseTotal/count
            avgTurnaroundTime = turnaroundTotal/count
            avgWaitTime = waitTotal/count
            
            print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))

            self.avg_wt.config(text="Average Waiting Time: " + str(avgWaitTime))
            self.avg_tat.config(text="Average Turnaround Time: " + str(avgTurnaroundTime))
            self.avg_rt.config(text="Average Response Time: " + str(avgResponseTime))

            


        elif selected_algorithm == "Round Robin":
            RR_joblist = []
            progress = 0.0
            totalBurstTime = 0

            for e in joblist:
                pid = joblist[e]['pid']
                jobnum = e
                processName = joblist[e]['processName']
                arrivalTime = joblist[e]['arrivalTime']
                burstTime = joblist[e]['burstTime']

                RR_joblist.append([pid, jobnum, processName, arrivalTime, burstTime])
                print('[PID', str(pid), '] Jobnum', str(jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            RR_joblist = sorted(RR_joblist, key=lambda e: e[3])

            for b in RR_joblist:
                totalBurstTime += b[4]

            print('Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = 1.0
            jobcount = len(RR_joblist)
            x = 10

            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1
            
            templist = []
            for e in RR_joblist:
                templist.append(e)

            runlist = []
            # runlist.append(templist[0])
            # templist.pop(0)

            time  = 0.0
            while jobcount > 0:    
                hasjob = 0
                index = 0
                for e in templist:
                    if time >= e[3]:
                        runlist.append(templist[index])
                        templist.pop(index)
                    index+=1

                if len(runlist) != 0:
                    job = runlist.pop(0)
                    hasjob = 1
                    pid = job[0]
                    jobnum  = job[1]
                    processName = job[2]
                    arrtime = job[3]
                    burtime = float(job[4])

                    if response[jobnum] == -1:
                        response[jobnum] = time

                    currwait = time - lastran[jobnum]
                    wait[jobnum] += currwait

                if len(runlist) == 0 and hasjob == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (time, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                elif burtime > quantum:
                    burtime -= quantum
                    ranfor = quantum
                    print('  [ time %3d ] Run job %3d for %.2f secs' % (time, jobnum, ranfor))
                    runlist.append([pid, jobnum, processName, arrtime, burtime])

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(job[0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)
                else:
                    ranfor = burtime
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (time, jobnum, ranfor, time + ranfor))
                    turnaround[jobnum] = time + ranfor
                    jobcount -= 1

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(job[0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)
                    
                time += ranfor
                lastran[jobnum] = time

                
                sleep(0.3)

            print('\nFinal statistics:')

            turnaroundTotal = 0.0
            waitTotal       = 0.0
            responseTotal   = 0.0

            for i in range(0,len(RR_joblist)):
                turnaroundTotal += turnaround[i]
                responseTotal += response[i]
                waitTotal += wait[i]
                print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i]))

            count = len(RR_joblist)
            avgResponseTime = responseTotal/count
            avgTurnaroundTime = turnaroundTotal/count
            avgWaitTime = waitTotal/count
            
            print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))

            


        elif selected_algorithm == "SRTF":
            print("a")

            


        elif selected_algorithm == "MLFQ":
            print("a")

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

        self.add_button = ttk.Button(input_frame, text="Add Process", command=self.getProcessInfo)
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

        self.run_button = ttk.Button(button_frame, text="Run Scheduling", command=self.start_thread)
        self.clear_button = ttk.Button(button_frame, text="Clear Processes", command=self.clearProcesses)
        self.exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)

        self.run_button.grid(row=0, column=0, padx=10)
        self.clear_button.grid(row=0, column=1, padx=10)
        self.exit_button.grid(row=0, column=2, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()