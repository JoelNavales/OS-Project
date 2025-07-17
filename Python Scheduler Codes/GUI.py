import tkinter as tk
from tkinter import ttk, messagebox, StringVar, OptionMenu

import random
import sys
from time import sleep
import threading

#Hardcode defaults
numQueues = 4
timeSlice = 1
timeAllotment = 1
highestQueue = 0
numberOfJobs = 5

#User inputs
mlfqrr_timeslice = timeSlice
mlfq_timeallotment = timeAllotment
all_numberofjobs = 0

#Initialize joblist
all_joblist = {}

#Initialize queues for mlfq
queue = {}
for q in range(numQueues):
    queue[q] = []

#Initialize runlist for mlfq
MLFQ_runlist = {}

class CPUSchedulerGUI:

    def dequeueProcess(self):
        selected = self.status_tree.selection()
        for item in selected:
            self.status_tree.delete(item)
            for pid, item_id in list(self.process_items.items()):
                if item_id == item:
                    self.process_items.pop(pid)
                    break

    def getRandomColor(self):
        r = random.randint(150, 255)
        g = random.randint(150, 255)
        b = random.randint(150, 255)
    
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def Abort(self, str):
        sys.stderr.write(str + '\n')
        exit(1)

    def FindQueue(self):
        q = highestQueue
        while q < 4:
            if len(queue[q]) > 0:
                return q
            q += 1
        if len(queue[3]) > 0:
            return 3
        return -1

    def updateNextQueueMLFQ(self, algo_runlist, currQueue):
        if len(algo_runlist[currQueue]) > 1:
            nextJob = algo_runlist[currQueue][1]
            self.queue_label.config(text="PID of Next in CPU Queue: " + str(all_joblist[nextJob]['pid']))
        elif len(algo_runlist) >= 0:
            self.queue_label.config(text="PID of Next in CPU Queue: N/A")

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
        global all_numberofjobs
        global all_joblist
        global mlfqrr_timeslice
        global mlfq_timeallotment

        all_numberofjobs = self.num_jobs_entry.get()
        mlfqrr_timeslice = self.time_slice_entry.get()
        mlfq_timeallotment = self.allotment_entry.get()

        if all_numberofjobs == '':
            all_numberofjobs = numberOfJobs

        if mlfqrr_timeslice == '':
            mlfqrr_timeslice = timeSlice
        
        if mlfq_timeallotment == '':
            mlfq_timeallotment = timeAllotment

        try:
            all_numberofjobs = int(all_numberofjobs)

            if all_numberofjobs <= 0:
                messagebox.showerror("Error", "Please enter Number of Jobs greater than 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid integer", icon = 'error')
            return
        
        try:
            mlfqrr_timeslice = int(mlfqrr_timeslice)

            if mlfqrr_timeslice <= 0:
                messagebox.showerror("Error", "Please enter Time Slice greater than 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid integer", icon = 'error')
            return
        
        try:
            mlfq_timeallotment = int(mlfq_timeallotment)

            if mlfq_timeallotment <= 0:
                messagebox.showerror("Error", "Please enter Time Allotment greater than 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid integer", icon = 'error')
            return

        for genpro_jobnum in range(0,all_numberofjobs):
            pid = genpro_jobnum + 5
            processName = "Job " + str(genpro_jobnum)
            arrivalTime = int(10 * random.random()) + 1
            burstTime = int(10 * random.random()) + 1
            color = self.getRandomColor()

            all_joblist[genpro_jobnum] = {'currPri':highestQueue, 'ticksLeft':mlfqrr_timeslice,
                    'allotLeft':mlfq_timeallotment, 'arrivalTime':arrivalTime,
                    'burstTime':burstTime, 'timeLeft':burstTime, 'firstRun':-1, 'pid': pid, 'processName': processName, 'color': color} 
            
            if arrivalTime not in MLFQ_runlist:
                MLFQ_runlist[arrivalTime] = []
            MLFQ_runlist[arrivalTime].append((genpro_jobnum, 'First run'))

            data = {"PID": pid, "Name": processName, "Arrival": arrivalTime, "Burst": burstTime, "Completion": "-", "Turn Around Time": "-", "Response Time": "-", "Status": "Waiting"}
            self.process_data.append(data)
            item_id = self.status_tree.insert("", tk.END, values=(pid, processName, arrivalTime, burstTime, "-", "-", "-", "Waiting"))
            self.process_items[pid] = item_id
        
        self.action_label.config(text = "Processes has been successfully added to the queue.")

    def clearProcesses(self):
        global all_joblist
        global mlfqrr_timeslice
        global mlfq_timeallotment
        global all_numberofjobs
        global queue
        global MLFQ_runlist

        self.status_tree.delete(*self.status_tree.get_children())
        self.process_data.clear()
        self.process_items.clear()

        self.gantt_chart.delete("all")

        all_joblist = {}
        mlfqrr_timeslice = timeSlice
        mlfq_timeallotment = timeAllotment
        all_numberofjobs = 0
        queue = {}
        for q in range(numQueues):
            queue[q] = []
        MLFQ_runlist = {}

        self.avg_wt.config(text="Average Waiting Time: 0.00")
        self.avg_tat.config(text="Average Turnaround Time: 0.00")
        self.avg_rt.config(text="Average Response Time: 0.00")
        self.overall_progress["value"] = 0

        self.action_label.config(text = "Processes Successfully Cleared.")

    def getProcessInfo(self):
        global all_numberofjobs
        global all_joblist
        global mlfqrr_timeslice
        global mlfq_timeallotment

        processName = self.pid_entry.get()
        if processName == '':
            processName = "Job " + str(all_numberofjobs)

        mlfqrr_timeslice = self.time_slice_entry.get()
        if mlfqrr_timeslice == '':
            mlfqrr_timeslice = timeSlice

        mlfq_timeallotment = self.allotment_entry.get()
        if mlfq_timeallotment == '':
            mlfq_timeallotment = timeAllotment

        arrivalTime = self.arrival_entry.get()
        burstTime = self.burst_entry.get()
        pid = all_numberofjobs + 5

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

        try:
            mlfqrr_timeslice = int(mlfqrr_timeslice)

            if mlfqrr_timeslice <= 0:
                messagebox.showerror("Error", "Please enter Time Slice greater than 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid integer", icon = 'error')
            return
        
        try:
            mlfq_timeallotment = int(mlfq_timeallotment)

            if mlfq_timeallotment <= 0:
                messagebox.showerror("Error", "Please enter Time Allotment greater than 0", icon = 'error')
        except:
            messagebox.showerror("Error", "Please enter a valid integer", icon = 'error')
            return

        color = self.getRandomColor()

        all_joblist[all_numberofjobs] = {'currPri':highestQueue, 'ticksLeft':mlfqrr_timeslice,
                'allotLeft':mlfq_timeallotment, 'arrivalTime':arrivalTime,
                'burstTime':burstTime, 'timeLeft':burstTime, 'firstRun':-1, 'pid': pid, 'processName': processName, 'color': color} 
        
        if arrivalTime not in MLFQ_runlist:
            MLFQ_runlist[arrivalTime] = []
        MLFQ_runlist[arrivalTime].append((all_numberofjobs, 'First run'))
        
        data = {"PID": pid, "Name": processName, "Arrival": arrivalTime, "Burst": burstTime, "Completion": "-", "Turn Around Time": "-", "Response Time": "-", "Status": "Waiting"}
        self.process_data.append(data)
        item_id = self.status_tree.insert("", tk.END, values=(pid, processName, arrivalTime, burstTime, "-", "-", "-", "Waiting"))
        self.process_items[pid] = item_id
        self.action_label.config(text = processName +  " has been successfully added to the queue.")
        
        all_numberofjobs+=1

    def run_scheduling(self):
        global all_joblist

        self.gantt_chart.delete("all")
        selected_algorithm = self.clicked.get()
        self.action_label.config(text=f"Action: Running {selected_algorithm} scheduling...")
        messagebox.showinfo("Selected Algorithm", f"Running {selected_algorithm} scheduling...")

        if selected_algorithm == "FIFO":
            FIFO_joblist = []

            #Initialize values for the progress bar
            progress = 0.0
            totalBurstTime = 0

            #Copy only needed info from all_joblist
            for e in all_joblist:
                pid = all_joblist[e]['pid']
                FIFO_jobnum = e
                processName = all_joblist[e]['processName']
                arrivalTime = all_joblist[e]['arrivalTime']
                burstTime = all_joblist[e]['burstTime']
                color = all_joblist[e]['color']

                FIFO_joblist.append([pid, FIFO_jobnum, processName, arrivalTime, burstTime, color])
                print('[PID', str(pid), '] Jobnum', str(FIFO_jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            #Sorts the joblist based on their arrival time
            FIFO_joblist = sorted(FIFO_joblist, key=lambda e: e[3])

            #Get total burst time for progress bar
            for b in FIFO_joblist:
                totalBurstTime += b[4]
            x = 10

            print('\n Debug Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = timeSlice
            jobcount = len(FIFO_joblist)

            #Stores data of every job
            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1
            
            #To keep track on which jobs are in the queue and not
            runlist = []
            templist = []
            for e in FIFO_joblist:
                templist.append(e)

            index = 0
            for e in templist:
                if 0 == e[3]:
                    runlist.append(templist[index])
                    templist.pop(index)
                    
                index+=1

            scheduler_time  = 0.0
            while jobcount > 0:  
                if len(runlist) != 0:
                    FIFO_jobnum = runlist[0][1]

                    #Sets response time of job
                    if response[runlist[0][1]] == -1:
                        response[runlist[0][1]] = scheduler_time

                        for data in self.process_data:
                            pid = data["PID"]

                            if pid == runlist[0][0]:
                                data["Response Time"] = str(response[runlist[0][1]])
                                item_id = self.process_items[pid]
                                self.status_tree.item(item_id, values=(
                                    pid, data["Name"], data["Arrival"], data["Burst"],
                                    data["Completion"], data["Turn Around Time"], str(response[runlist[0][1]]), data["Status"]
                                ))


                    currwait = scheduler_time - lastran[runlist[0][1]]
                    wait[runlist[0][1]] += currwait

                #IF no job is in the run queue
                if len(runlist) == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (scheduler_time, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                    for data in self.process_data:
                        pid = data["PID"]
                        if data["Status"] != "Completed":
                            data["Status"] = "Waiting"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Waiting"
                            ))

                elif runlist[0][4] > quantum:
                    runlist[0][4] -= quantum
                    ranfor = quantum

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=runlist[0][5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width

                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid = data["PID"]

                        if pid == runlist[0][0]:
                            data["Status"] = "Running"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Running"
                            ))

                    print('  [ time %3d ] Run job %3d for %.2f secs' % (scheduler_time, runlist[0][1], ranfor))
                    
                elif runlist[0][4] <= quantum:
                    ranfor = runlist[0][4]
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (scheduler_time, runlist[0][1], ranfor, scheduler_time + ranfor))
                    turnaround[runlist[0][1]] = scheduler_time + ranfor

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=runlist[0][5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width

                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid = data["PID"]
                        data["Turn Around Time"] = str(turnaround[runlist[0][1]])
                        if pid == runlist[0][0]:
                            data["Status"] = "Completed"
                            data["Completion"] = str(scheduler_time)
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                str(scheduler_time), str(turnaround[runlist[0][1]]), data["Response Time"], "Completed"
                            ))

                    runlist.pop(0)
                    jobcount -= 1
                    
                scheduler_time += ranfor
                lastran[FIFO_jobnum] = scheduler_time

                index = 0
                for e in templist:
                    #If scheduler time is >= arrival time, add to run queue
                    if scheduler_time >= e[3]:
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

            #Initialize values for the progress bar
            progress = 0.0
            totalBurstTime = 0

            #Copy only needed info from all_joblist
            for e in all_joblist:
                pid = all_joblist[e]['pid']
                SJF_jobnum = e
                processName = all_joblist[e]['processName']
                arrivalTime = all_joblist[e]['arrivalTime']
                burstTime = all_joblist[e]['burstTime']
                color = all_joblist[e]['color']

                SJF_joblist.append([pid, SJF_jobnum, processName, arrivalTime, burstTime, color])
                print('[PID', str(pid), '] SJF_jobnum', str(SJF_jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            #Sorts the joblist based on their arrival time then their burst time
            SJF_joblist = sorted(SJF_joblist, key=lambda e: (e[3], e[4]))

            #Get total burst time for progress bar
            for b in SJF_joblist:
                totalBurstTime += b[4]
            x = 10

            print('\n Debug Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = timeSlice
            jobcount = len(SJF_joblist)
            
            #Stores data of every job
            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1

            #To keep track on which jobs are in the queue and not
            runlist = []
            templist = []
            for e in SJF_joblist:
                templist.append(e)

            index = 0
            for e in templist:
                if 0 == e[3]:
                    runlist.append(templist[index])
                    templist.pop(index)
                    break
                    
                index+=1

            scheduler_time  = 0.0
            while jobcount > 0:  
                if len(runlist) != 0:
                    SJF_jobnum =  runlist[0][1]

                    #Sets response time of job
                    if response[runlist[0][1]] == -1:
                        response[runlist[0][1]] = scheduler_time

                        for data in self.process_data:
                            pid = data["PID"]

                            if pid == runlist[0][0]:
                                data["Response Time"] = str(response[runlist[0][1]])
                                item_id = self.process_items[pid]
                                self.status_tree.item(item_id, values=(
                                    pid, data["Name"], data["Arrival"], data["Burst"],
                                    data["Completion"], data["Turn Around Time"], str(response[runlist[0][1]]), data["Status"]
                                ))

                    currwait = scheduler_time - lastran[runlist[0][1]]
                    wait[runlist[0][1]] += currwait

                #IF no job is in the run queue
                if len(runlist) == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (scheduler_time, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                    for data in self.process_data:
                        pid = data["PID"]

                        if data["Status"] != "Completed":
                            data["Status"] = "Waiting"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Waiting"
                            ))

                elif runlist[0][4] > quantum:
                    runlist[0][4] -= quantum
                    ranfor = quantum

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=runlist[0][5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid = data["PID"]

                        if pid == runlist[0][0]:
                            data["Status"] = "Running"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Running"
                            ))

                    print('  [ time %3d ] Run job %3d for %.2f secs' % (scheduler_time, runlist[0][1], ranfor))
                    
                elif runlist[0][4] <= quantum:
                    ranfor = runlist[0][4]
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (scheduler_time, runlist[0][1], ranfor, scheduler_time + ranfor))
                    turnaround[runlist[0][1]] = scheduler_time + ranfor

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=runlist[0][5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid = data["PID"]
                        data["Turn Around Time"] = str(turnaround[runlist[0][1]])
                        if pid == runlist[0][0]:
                            data["Status"] = "Completed"
                            data["Completion"] = str(scheduler_time)
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                str(scheduler_time), str(turnaround[runlist[0][1]]), data["Response Time"], "Completed"
                            ))
                    
                    runlist.pop(0)

                    if len(runlist) != 0:
                        runlist = sorted(runlist, key=lambda e: e[4])

                    jobcount -= 1
                    
                scheduler_time += ranfor
                lastran[SJF_jobnum] = scheduler_time

                index = 0
                for e in templist:
                    #If scheduler time is >= arrival time, add to run queue
                    if scheduler_time >= e[3]:
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

            

        elif selected_algorithm == "RR":
            RR_joblist = []

            #Initialize values for the progress bar
            progress = 0.0
            totalBurstTime = 0

            #Copy only needed info from all_joblist
            for e in all_joblist:
                pid = all_joblist[e]['pid']
                RR_jobnum = e
                processName = all_joblist[e]['processName']
                arrivalTime = all_joblist[e]['arrivalTime']
                burstTime = all_joblist[e]['burstTime']
                color = all_joblist[e]['color']

                RR_joblist.append([pid, RR_jobnum, processName, arrivalTime, burstTime, color])
                print('[PID', str(pid), '] RR_jobnum', str(RR_jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            #Sorts the joblist based on their arrival time
            RR_joblist = sorted(RR_joblist, key=lambda e: e[3])

            #Get total burst time for progress bar
            for b in RR_joblist:
                totalBurstTime += b[4]
            x = 10

            print('\n Debug Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = mlfqrr_timeslice
            jobcount = len(RR_joblist)
            
            #Stores data of every job
            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1
            
            #To keep track on which jobs are in the queue and not
            runlist = []
            templist = []
            for e in RR_joblist:
                templist.append(e)

            scheduler_time  = 0.0
            while jobcount > 0:
                #Indicates if the scheduler has a job in queue
                hasjob = 0

                
                for e in RR_joblist:
                    index = 0
                    for e in templist:
                        #If scheduler time is >= arrival time, add to run queue
                        if scheduler_time >= e[3]:
                            runlist.append(templist[index])
                            templist.pop(index)
                            continue
                        index+=1

                #If there is a job in run queue
                if len(runlist) != 0:
                    job = runlist.pop(0)
                    hasjob = 1
                    pid = job[0]
                    RR_jobnum  = job[1]
                    processName = job[2]
                    arrtime = job[3]
                    burtime = float(job[4])
                    color = job[5]

                    if response[RR_jobnum] == -1:
                        response[RR_jobnum] = scheduler_time

                        for data in self.process_data:
                            pid_tree = data["PID"]

                            if pid_tree == job[0]:
                                data["Response Time"] = str(response[RR_jobnum])
                                item_id = self.process_items[pid_tree]
                                self.status_tree.item(item_id, values=(
                                    pid_tree, data["Name"], data["Arrival"], data["Burst"],
                                    data["Completion"], data["Turn Around Time"], str(response[RR_jobnum]), data["Status"]
                                ))

                    currwait = scheduler_time - lastran[RR_jobnum]
                    wait[RR_jobnum] += currwait

                #If there are no job in run queue and scheduler also no job
                if len(runlist) == 0 and hasjob == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (scheduler_time, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                    for data in self.process_data:
                        pid_tree = data["PID"]

                        if data["Status"] != "Completed":
                            data["Status"] = "Waiting"
                            item_id = self.process_items[pid_tree]
                            self.status_tree.item(item_id, values=(
                                pid_tree, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Waiting"
                            ))

                elif burtime > quantum:
                    burtime -= quantum
                    ranfor = quantum
                    print('  [ time %3d ] Run job %3d for %.2f secs' % (scheduler_time, RR_jobnum, ranfor))
                    runlist.append([pid, RR_jobnum, processName, arrtime, burtime, color])

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=job[5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(job[0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid_tree = data["PID"]

                        if pid_tree == job[0]:
                            data["Status"] = "Running"
                            item_id = self.process_items[pid_tree]
                            self.status_tree.item(item_id, values=(
                                pid_tree, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Running"
                            ))
                else:
                    ranfor = burtime
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (scheduler_time, RR_jobnum, ranfor, scheduler_time + ranfor))
                    turnaround[RR_jobnum] = scheduler_time + ranfor
                    jobcount -= 1

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=job[5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(job[0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid_tree = data["PID"]
                        data["Turn Around Time"] = str(turnaround[RR_jobnum])
                        if pid_tree == job[0]:
                            data["Status"] = "Completed"
                            data["Completion"] = str(scheduler_time)
                            item_id = self.process_items[pid_tree]
                            self.status_tree.item(item_id, values=(
                                pid_tree, data["Name"], data["Arrival"], data["Burst"],
                                str(scheduler_time), str(turnaround[RR_jobnum]), data["Response Time"], "Completed"
                            ))
                    
                scheduler_time += ranfor
                lastran[RR_jobnum] = scheduler_time

                
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

            self.avg_wt.config(text="Average Waiting Time: " + str(avgWaitTime))
            self.avg_tat.config(text="Average Turnaround Time: " + str(avgTurnaroundTime))
            self.avg_rt.config(text="Average Response Time: " + str(avgResponseTime))
            


        elif selected_algorithm == "SRTF":
            SRTF_joblist = []

            #Initialize values for the progress bar
            progress = 0.0
            totalBurstTime = 0

            #Copy only needed info from all_joblist
            for e in all_joblist:
                pid = all_joblist[e]['pid']
                SRTF_jobnum = e
                processName = all_joblist[e]['processName']
                arrivalTime = all_joblist[e]['arrivalTime']
                burstTime = all_joblist[e]['burstTime']
                color = all_joblist[e]['color']

                SRTF_joblist.append([pid, SRTF_jobnum, processName, arrivalTime, burstTime, color])
                print('[PID', str(pid), '] Jobnum', str(SRTF_jobnum), 'Job Name ', processName, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')

            #Sorts the joblist based on their arrival time
            SRTF_joblist = sorted(SRTF_joblist, key=lambda e: e[3])

            #Get total burst time for progress bar
            for b in SRTF_joblist:
                totalBurstTime += b[4]
            x = 10

            print('\n Debug Execution trace:')
            turnaround = {}
            response = {}
            lastran = {}
            wait = {}
            quantum  = timeSlice
            jobcount = len(SRTF_joblist)
            
            #Stores data of every job
            for i in range(0,jobcount):
                lastran[i] = 0.0
                wait[i] = 0.0
                turnaround[i] = 0.0
                response[i] = -1

            #To keep track on which jobs are in the queue and not
            runlist = []
            templist = []
            for e in SRTF_joblist:
                templist.append(e)

            index = 0
            for e in templist:
                if 0 == e[3]:
                    runlist.append(templist[index])
                    templist.pop(index)
                    break
                    
                index+=1

            scheduler_time  = 0.0
            while jobcount > 0:  
                if len(runlist) != 0:
                    SRTF_jobnum = runlist[0][1]

                    #Sets response time of job
                    if response[runlist[0][1]] == -1:
                        response[runlist[0][1]] = scheduler_time

                        for data in self.process_data:
                            pid = data["PID"]

                            if pid == runlist[0][0]:
                                data["Response Time"] = str(response[runlist[0][1]])
                                item_id = self.process_items[pid]
                                self.status_tree.item(item_id, values=(
                                    pid, data["Name"], data["Arrival"], data["Burst"],
                                    data["Completion"], data["Turn Around Time"], str(response[runlist[0][1]]), data["Status"]
                                ))

                    currwait = scheduler_time - lastran[runlist[0][1]]
                    wait[runlist[0][1]] += currwait

                #IF no job is in the run queue
                if len(runlist) == 0:
                    ranfor = quantum
                    print('  [ time %3d ] CPU idle for %.2f secs' % (scheduler_time, ranfor))

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                    for data in self.process_data:
                        pid = data["PID"]
                        if data["Status"] != "Completed":
                            data["Status"] = "Waiting"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Waiting"
                            ))

                elif runlist[0][4] > quantum:
                    runlist[0][4] -= quantum
                    ranfor = quantum

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=runlist[0][5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid = data["PID"]

                        if pid == runlist[0][0]:
                            data["Status"] = "Running"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Running"
                            ))

                    print('  [ time %3d ] Run job %3d for %.2f secs' % (scheduler_time, runlist[0][1], ranfor))
                    
                elif runlist[0][4] <= quantum:
                    ranfor = runlist[0][4]
                    print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (scheduler_time, runlist[0][1], ranfor, scheduler_time + ranfor))
                    turnaround[runlist[0][1]] = scheduler_time + ranfor

                    #Update Gantt Chart
                    width = ranfor * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=runlist[0][5])
                    self.gantt_chart.create_text(x + width / 2, 25, text=str(runlist[0][0]))
                    x += width
                    progress = self.updateOverallProgress(totalBurstTime, progress, ranfor)
                    self.updateNextQueue(runlist)

                    for data in self.process_data:
                        pid = data["PID"]
                        data["Turn Around Time"] = str(turnaround[runlist[0][1]])
                        if pid == runlist[0][0]:
                            data["Status"] = "Completed"
                            data["Completion"] = str(scheduler_time)
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                str(scheduler_time), str(turnaround[runlist[0][1]]), data["Response Time"], "Completed"
                            ))
                    
                    runlist.pop(0)
                    jobcount -= 1
                    
                scheduler_time += ranfor
                lastran[SRTF_jobnum] = scheduler_time

                index = 0
                for e in templist:
                    #If scheduler time is >= arrival time, add to run queue
                    if scheduler_time >= e[3]:
                        if len(runlist) == 0:
                            runlist.append(templist[index])
                            templist.pop(index)
                            runlist = sorted(runlist, key=lambda b: b[4])
                            break
                        elif runlist[0][4] >= e[4]:
                            runlist.append(templist[index])
                            templist.pop(index)
                            runlist = sorted(runlist, key=lambda b: b[4])
                            break
                    
                    index+=1
                
                sleep(0.3)

            print('\nFinal statistics:')

            turnaroundTotal = 0.0
            waitTotal       = 0.0
            responseTotal   = 0.0

            for i in range(0,len(SRTF_joblist)):
                turnaroundTotal += turnaround[i]
                responseTotal += response[i]
                waitTotal += wait[i]
                print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i]))

            count = len(SRTF_joblist)
            avgResponseTime = responseTotal/count
            avgTurnaroundTime = turnaroundTotal/count
            avgWaitTime = waitTotal/count
            
            print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))

            self.avg_wt.config(text="Average Waiting Time: " + str(avgWaitTime))
            self.avg_tat.config(text="Average Turnaround Time: " + str(avgTurnaroundTime))
            self.avg_rt.config(text="Average Response Time: " + str(avgResponseTime))

            

        elif selected_algorithm == "MLFQ":
            #Initialize values for the progress bar
            progress = 0.0
            totalBurstTime = 0
            for b in all_joblist:
                totalBurstTime += all_joblist[b]['burstTime']
            x = 10

            jobnum = all_numberofjobs

            currTime = 0
            totalJobs = len(all_joblist)
            finishedJobs = 0

            print('\nExecution Trace:\n')

            while finishedJobs < totalJobs:
                
                print(MLFQ_runlist)
                if currTime in MLFQ_runlist:
                    for (j, type) in MLFQ_runlist[currTime]:
                        print(j)
                        q = all_joblist[j]['currPri']
                        print('[ time %d ] JOB %d Begins' % (currTime, j))
                        if type == 'First run':
                            queue[q].append(j)
                        else:
                            queue[q].insert(0, j)

                currQueue = self.FindQueue()
                if currQueue == -1:
                    print('[ time %d ] IDLE' % (currTime))

                    #Update Gantt Chart
                    width = mlfqrr_timeslice * 40
                    self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill="skyblue")
                    self.gantt_chart.create_text(x + width / 2, 25, text="IDLE")
                    x += width

                    for data in self.process_data:
                        pid = data["PID"]
                        if data["Status"] != "Completed":
                            data["Status"] = "Waiting"
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                data["Completion"], data["Turn Around Time"], data["Response Time"], "Waiting"
                            ))

                    currTime += 1
                    continue

                currJob = queue[currQueue][0]
                if all_joblist[currJob]['currPri'] != currQueue:
                    self.Abort('currPri[%d] does not match currQueue[%d]' % (all_joblist[currJob]['currPri'], currQueue))

                all_joblist[currJob]['timeLeft']  -= 1
                all_joblist[currJob]['ticksLeft'] -= 1

                if all_joblist[currJob]['firstRun'] == -1:
                    all_joblist[currJob]['firstRun'] = currTime

                burstTime   = all_joblist[currJob]['burstTime']
                ticksLeft = all_joblist[currJob]['ticksLeft']
                allotLeft = all_joblist[currJob]['allotLeft']
                timeLeft  = all_joblist[currJob]['timeLeft']

                #Update Gantt Chart
                width = mlfqrr_timeslice * 40
                self.gantt_chart.create_rectangle(x, 10, x + width, 40, fill=all_joblist[currJob]['color'])
                self.gantt_chart.create_text(x + width / 2, 25, text="Q " + str(currQueue) + "\n" + str(all_joblist[currJob]['pid']))
                x += width
                progress = self.updateOverallProgress(totalBurstTime, progress, mlfqrr_timeslice)
                self.updateNextQueueMLFQ(queue, currQueue)

                for data in self.process_data:
                            pid = data["PID"]

                            if pid == all_joblist[currJob]['pid']:
                                response   = all_joblist[currJob]['firstRun'] - all_joblist[currJob]['arrivalTime']
                                data["Response Time"] = str(response)
                                data["Status"] = "Running"
                                item_id = self.process_items[pid]
                                self.status_tree.item(item_id, values=(
                                    pid, data["Name"], data["Arrival"], data["Burst"],
                                    data["Completion"], data["Turn Around Time"], str(response), "Running"
                                ))

                print('[ time %d ] Run JOB %d at PRIORITY %d [ TICKS %d ALLOT %d TIME %d (of %d) ]' % \
                    (currTime, currJob, currQueue, ticksLeft, allotLeft, timeLeft, burstTime))

                if timeLeft < 0:
                    self.Abort('Error: should never have less than 0 time left to run')


                # UPDATE TIME
                currTime += 1

                # CHECK FOR JOB ENDING
                if timeLeft == 0:
                    print('[ time %d ] FINISHED JOB %d' % (currTime, currJob))
                    finishedJobs += 1
                    all_joblist[currJob]['endTime'] = currTime

                    for data in self.process_data:
                        pid = data["PID"]
                        turnaround = all_joblist[currJob]['endTime'] - all_joblist[currJob]['arrivalTime']
                        data["Turn Around Time"] = str(turnaround)

                        if pid == all_joblist[currJob]['pid']:
                            data["Status"] = "Completed"
                            data["Completion"] = str(all_joblist[currJob]['endTime'])
                            item_id = self.process_items[pid]
                            self.status_tree.item(item_id, values=(
                                pid, data["Name"], data["Arrival"], data["Burst"],
                                str(currTime), str(turnaround), data["Response Time"], "Completed"
                            ))
                    
                    done = queue[currQueue].pop(0)

                    assert(done == currJob)
                    sleep(0.3)
                    continue

                if ticksLeft == 0:
                    desched = queue[currQueue].pop(0)
                    assert(desched == currJob)

                    all_joblist[currJob]['allotLeft'] = all_joblist[currJob]['allotLeft'] - 1

                    if all_joblist[currJob]['allotLeft'] == 0:
                        # This job is done at this priority queue
                        if currQueue < 3:
                            # So change its priority queue
                            all_joblist[currJob]['currPri']   = currQueue + 1
                            all_joblist[currJob]['ticksLeft'] = mlfqrr_timeslice
                            all_joblist[currJob]['allotLeft'] = mlfq_timeallotment
                            queue[currQueue+1].append(currJob)

                        else:
                            all_joblist[currJob]['ticksLeft'] = mlfqrr_timeslice
                            all_joblist[currJob]['allotLeft'] = mlfq_timeallotment
                            queue[currQueue].append(currJob)

                    else:
                        all_joblist[currJob]['ticksLeft'] = mlfqrr_timeslice
                        queue[currQueue].append(currJob)
                
                sleep(0.3)
                

            # print out statistics
            print('')
            print('Final statistics:')
            responseSum   = 0
            turnaroundSum = 0
            for i in range(jobnum):
                response   = all_joblist[i]['firstRun'] - all_joblist[i]['arrivalTime']
                turnaround = all_joblist[i]['endTime'] - all_joblist[i]['arrivalTime']
                print('  Job %2d: arrivalTime %3d - response %3d - turnaround %3d' % (i, all_joblist[i]['arrivalTime'], response, turnaround))
                responseSum   += response
                turnaroundSum += turnaround

            

            print('\n  Avg %2d: arrivalTime n/a - response %.2f - turnaround %.2f' % (i, float(responseSum)/jobnum, float(turnaroundSum)/jobnum))
            print('\n')

            avgResponseTime = float(responseSum)/jobnum
            avgTurnaroundTime = float(turnaroundSum)/jobnum
            avgWaitTime = "N/A"

            self.avg_wt.config(text="Average Waiting Time: " + avgWaitTime)
            self.avg_tat.config(text="Average Turnaround Time: " + str(avgTurnaroundTime))
            self.avg_rt.config(text="Average Response Time: " + str(avgResponseTime))

        self.action_label.config(text=f"Action: Finished running with {selected_algorithm} scheduling.")

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
        self.options = ["FIFO", "SJF", "SRTF", "RR", "MLFQ"]
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()