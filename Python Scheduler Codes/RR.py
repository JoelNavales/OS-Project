import random

def returnArrivalTime(e):
    return e[2]

def generateProcesses(numOfJobs, joblist):
    for jobnum in range(0,numOfJobs):
        pid = jobnum + 5
#        arrivalTime = 0
        arrivalTime = int(10 * random.random()) + 1
        burstTime = int(10 * random.random()) + 1
        joblist.append([pid, jobnum, arrivalTime, burstTime])
        print('[PID', str(pid), '] Job', jobnum, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')
    print('\n')          
    return joblist

def printExecTrace(joblist):
    print('Execution trace:')
    turnaround = {}
    response = {}
    lastran = {}
    wait = {}
    quantum  = 1.0
    jobcount = len(joblist)

    for i in range(0,jobcount):
        lastran[i] = 0.0
        wait[i] = 0.0
        turnaround[i] = 0.0
        response[i] = -1
    
    templist = []
    for e in joblist:
        templist.append(e)

    runlist = []
    runlist.append(templist[0])
    templist.pop(0)

    time  = 0.0
    while jobcount > 0:    
        for e in templist:
            if time >= e[2]:
                runlist.append(e)
                templist.pop(e.index(e[0]))

        job = runlist.pop(0)
        pid = job[0]
        jobnum  = job[1]
        arrtime = job[2]
        burtime = float(job[3])

        if response[jobnum] == -1:
            response[jobnum] = time

        currwait = time - lastran[jobnum]
        wait[jobnum] += currwait

        if burtime > quantum:
            burtime -= quantum
            ranfor = quantum
            print('  [ time %3d ] Run job %3d for %.2f secs' % (time, jobnum, ranfor))
            runlist.append([pid, jobnum, arrtime, burtime])
        else:
            ranfor = burtime
            print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (time, jobnum, ranfor, time + ranfor))
            turnaround[jobnum] = time + ranfor
            jobcount -= 1
            
        time += ranfor
        lastran[jobnum] = time

    print('\nFinal statistics:')

    turnaroundTotal = 0.0
    waitTotal       = 0.0
    responseTotal   = 0.0

    for i in range(0,len(joblist)):
        turnaroundTotal += turnaround[i]
        responseTotal += response[i]
        waitTotal += wait[i]
        print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i]))

    count = len(joblist)
    avgResponseTime = responseTotal/count
    avgTurnaroundTime = turnaroundTotal/count
    avgWaitTime = waitTotal/count
    
    print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))
    
def main():
    joblist = []
    joblist = generateProcesses(5,joblist)
    joblist.sort(key=returnArrivalTime)
    printExecTrace(joblist)

#Run Main Function
main()